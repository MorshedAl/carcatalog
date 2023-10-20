from django.urls import path
from accounts.views import (
    UserCreateView,UserLoginView,
    LogoutView,UserProfileView,AdminDashboardView,
    AdminCarListdView,AdminOrderListdView,AdminOrderUpdateView,
    UserOrderListdView
)


urlpatterns = [
    path("registration/", UserCreateView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", UserProfileView.as_view(), name="profile"),
    path("admin/<int:pk>/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("admin/car/", AdminCarListdView.as_view(), name="admin_car"),
    path("admin/order/", AdminOrderListdView.as_view(), name="admin_order"),
    path("user/order/", UserOrderListdView.as_view(), name="user_order"),
    path("admin/order/<int:pk>/update/", AdminOrderUpdateView.as_view(), name="admin_order_update"),

]
