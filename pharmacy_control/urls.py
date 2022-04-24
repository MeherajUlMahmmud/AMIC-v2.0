from django.urls import path

from .views import *

urlpatterns = [
    path("", pharmacy_home_view, name="pharmacy-home"),
    path("medicine/<int:medicine_id>", pharmacy_medicine_view, name="medicine-details"),
    path("cart", pharmacy_cart_view, name="pharmacy-cart"),
    path("update-item/", updateItem, name="update-item"),
    path("cart/update-item/", updateItem, name="update-item"),
    path("proceed-order", proceed_order, name="proceed-order"),
    path("confirm-order/<str:pk>", confirm_order, name="confirm-order"),
    path("order-details/<str:pk>", order_details, name="order-details"),
]
