import os
from sslcommerz_lib import SSLCOMMERZ
from django.utils.crypto import get_random_string



def ssl_commerce_payment(request,address,cart):
    
    settings = { 'store_id': 'carca64f474c798521', 'store_pass': 'carca64f474c798521@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = cart.total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = get_random_string(14)
    post_body['success_url'] = f'{request.get_host()}/order/payment-success/'
    post_body['fail_url'] = f"{request.get_host()}/order/checkout/"
    post_body['cancel_url'] = "your cancel url"
    post_body['emi_option'] = 0
    post_body['cus_name'] = request.user.get_full_name
    post_body['cus_email'] = request.user.email
    post_body['cus_phone'] = request.user.phone_number
    post_body['cus_add1'] = address.address_line
    post_body['cus_city'] = address.city
    post_body['cus_country'] = address.country
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"
    post_body['value_a'] = cart.id
    post_body['value_b'] = address.id
    post_body['value_c'] = request.user.id


    response = sslcz.createSession(post_body)

    return response['GatewayPageURL']


