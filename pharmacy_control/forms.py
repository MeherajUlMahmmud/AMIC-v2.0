from django import forms
from django.forms import ModelForm

from user_control.constants import PAYMENT_METHOD_CHOICES

from .models import *


class OrderForm(ModelForm):  # a form to create an order
    payment_method = forms.CharField(
        widget=forms.Select(choices=PAYMENT_METHOD_CHOICES)
    )  # Add a payment method field

    class Meta:
        model = MedicineOrderModel  # Set the model to the OrderModel
        fields = [
            "payment_method",
            "phone",
            "transaction_id",
            "shipping_address",
        ]  # Set the fields to the above fields
