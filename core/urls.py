from django.urls import path
from core.views import (
    HomeView,CarDetailView,
    CarCreateView,CarListView,
    CarUpdateView,CarDeleteView
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("car/<int:pk>/<slug:slug>/", CarDetailView.as_view(), name="car_detail"),
    path("car/create/", CarCreateView.as_view(), name="car_create"),
    path("car/update/<int:pk>/", CarUpdateView.as_view(), name="car_update"),
    path("car/delete/<int:pk>/", CarDeleteView.as_view(), name="car_delete"),
    path("car/list/", CarListView.as_view(), name="car_list"),

]