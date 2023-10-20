from django.db import models

from accounts.models import Address, User
from core.models import Car

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_pay = models.BooleanField(default=False)
    create = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
    @property
    def total(self,*args, **kwargs):
        return sum([item.sub_total for item in self.cart_items.all()])
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_items')
    quentity = models.SmallIntegerField(("Quentity"))
    create = models.DateTimeField(("Created"), auto_now_add=True)

    @property
    def sub_total(self):
        return self.car.price*self.quentity
    
    def __str__(self):
        return f'{self.cart.user.email} order {self.car.title}'
    

class OrderStatus(models.TextChoices):
    PENDING = 'pending','pending'
    ACCEPT = 'accept','accept'
    ONTHEWAY = 'on_the_way','on the way'
    DELIVER = 'deliver','deliver'

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='orders')
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(("Status"), max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    create = models.DateTimeField(auto_now_add=True)


class PaymentDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length= 100)
    payment_method = models.CharField(max_length=100)
    paid_amount = models.DecimalField(max_digits=14,decimal_places=2)
    status = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add=True)

