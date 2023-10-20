
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy,reverse
from django.views import View
from django.views.generic import DetailView, CreateView, DeleteView
from accounts.mixin import LoginMixin
from accounts.models import Address, User


from core.models import Car
from orders.forms import AddressForm

from orders.models import Cart, CartItem, Order, PaymentDetails
from orders.payment import ssl_commerce_payment

# Create your views here.

class CartCreateView(View):
    model = Cart

    def get(self,request,car_id,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('login'))
        cart,created = Cart.objects.get_or_create(user = request.user,is_pay=False)
        car = Car.objects.get(pk=car_id)
        cart_item = cart.cart_items.filter(car__id=car_id).exists()
        if created or not cart_item:
            cart = CartItem.objects.create(
                cart = cart,
                car = car,
                quentity = 1
            )
            cart.save()
        else:
            item = cart.cart_items.get(car__id=car_id)
            item.quentity +=1
            item.save()


        return redirect(reverse('car_list'))

class CartDetailView(LoginMixin,DetailView):
    model = Cart
    template_name = "order/cart.html"
    context_object_name = 'cart'
    
    def get_object(self):
        return Cart.objects.get(user=self.request.user,is_pay=False)

class CartItemUpdate(LoginMixin,View):
    

    def cart_obj(self):
        return Cart.objects.get(user=self.request.user,is_pay=False)

    def delete_item(self,car_id):
        cart = self.cart_obj()
        cart.cart_items.get(car__id=car_id).delete()
    
    def add_quantity(self,car_id):
        cart = self.cart_obj()
        item = cart.cart_items.get(car__id=car_id)
        item.quentity +=1
        item.save()
    
    def minus_quantity(self,car_id):
        cart = self.cart_obj()
        item = cart.cart_items.get(car__id=car_id)
        item.quentity -=1
        item.save()





    def get(self,request,*args, **kwargs):
        id = self.kwargs.get('car_id')
        action = request.GET.get('action')
        if action=='add':
            self.add_quantity(id)
        elif action=="minus":
            self.minus_quantity(id)
        elif action=='delete':
            self.delete_item(id)

        return redirect(reverse_lazy('cart'))


class CheckoutView(LoginMixin,CreateView):
    model = Order
    template_name = 'order/checkout.html'
    form_class = AddressForm


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['address'] = Address.objects.filter(user=self.request.user)
        context['cart'] = Cart.objects.filter(user=self.request.user,is_pay=False).first()
        return context
    
    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            cart = Cart.objects.get(user=request.user,is_pay=False)
        
            
        return redirect(ssl_commerce_payment(request,address,cart))

    
@csrf_exempt
def payment_success(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    data = request.POST
    cart = Cart.objects.get(id=data.get('value_a'))
    address = Address.objects.get(id=data.get('value_b'))
    user = User.objects.get(id=data.get('value_c'))
    order = Order.objects.create(
        cart=cart,
        user = user,
        address = address
    )
    order.save()
    payment = PaymentDetails.objects.create(
        order = order,
        payment_id = data.get('tran_id'),
        payment_method = data.get('card_type').split('-')[1],
        paid_amount = float(data.get('amount')),
        status = 'Success'
    )
    payment.save()
    cart.is_pay = True
    cart.save()
    return render(request,'accounts/user/order_history.html',{'odere':order})



class OrderDeleteView(LoginMixin,DeleteView):
    model = Order
    template_name = "core/delete_car.html"

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return redirect(reverse_lazy('admin_order'))
        return redirect(reverse_lazy('user_order'))