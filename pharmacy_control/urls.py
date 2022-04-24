from django.urls import path

from .views import *

urlpatterns = [
    path("", pharmacy_home_view, name="pharmacy-home"),
    path(
        "medicine/<int:medicine_id>", pharmacy_medicine_view, name="pharmacy-medicine"
    ),
]
