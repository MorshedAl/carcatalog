from django import template

from orders.models import Cart

register = template.Library()

@register.inclusion_tag('common/cart_popup.html',takes_context=True)
def cart_popup(context):
    request = context['request']
    try:
        cart = Cart.objects.get(user=request.user,is_pay=False)
    except:
        cart = None
    return {
        'cart':cart
    }