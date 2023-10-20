from django.contrib import admin
from orders.models import *
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('id',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id',)

class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ('id',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',)


admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentDetails, PaymentDetailsAdmin)
