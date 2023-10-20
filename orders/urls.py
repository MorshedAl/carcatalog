from django.urls import path
from orders.views import (
    CartCreateView,CartDetailView,
    CartItemUpdate, CheckoutView,
    payment_success, OrderDeleteView
)


urlpatterns = [
    path("<int:car_id>/", CartCreateView.as_view(), name="cart_create"),
    path("cart/", CartDetailView.as_view(), name="cart"),
    path("item/<int:car_id>/update/", CartItemUpdate.as_view(), name="cart_item_update"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("payment-success/", payment_success, name="payment_success"),
    path("<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),

]
