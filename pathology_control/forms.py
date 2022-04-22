from .models import *
from django.forms import ModelForm
from user_control.constants import *
from django import forms


class TestBookingForm(ModelForm):
    """
    This form is used to create a new Test Booking.
    """

    gender = forms.CharField(widget=forms.Select(choices=GENDER_CHOICES))
    blood_group = forms.CharField(widget=forms.Select(choices=BLOOD_GROUP_CHOICES))
    date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    date_of_birth = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = TestModel
        fields = "__all__"
        exclude = ["user", "status", "created_at", "updated_at"]
