from .models import *
from django.forms import ModelForm
from user_control.constants import *
from django import forms


class CovidTestBookingForm(ModelForm):
    gender = forms.CharField(widget=forms.Select(choices=GENDER_CHOICES))
    date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = CovidTestModel
        fields = "__all__"
        exclude = ["user", "status", "created_at", "updated_at"]
