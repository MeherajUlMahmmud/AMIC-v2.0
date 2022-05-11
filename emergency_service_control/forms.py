from .models import *
from django.forms import ModelForm
from user_control.constants import *
from django import forms


class BloodRequestForm(ModelForm):
    gender = forms.CharField(widget=forms.Select(choices=GENDER_CHOICES))
    blood_group = forms.CharField(widget=forms.Select(choices=BLOOD_GROUP_CHOICES))
    needed_within = forms.DateField(
        required=True, widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = BloodRequestModel
        fields = "__all__"
        exclude = [
            "user",
            "is_active",
            "created_at",
            "updated_at",
        ]


class PlasmaRequestForm(ModelForm):
    gender = forms.CharField(widget=forms.Select(choices=GENDER_CHOICES))
    blood_group = forms.CharField(widget=forms.Select(choices=BLOOD_GROUP_CHOICES))
    needed_within = forms.DateField(
        required=True, widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = PlasmaRequestModel
        fields = "__all__"
        exclude = [
            "user",
            "is_active",
            "created_at",
            "updated_at",
        ]


class AmbulanceForm(ModelForm):
    class Meta:
        model = AmbulanceModel
        fields = "__all__"
        exclude = [
            "created_at",
            "updated_at",
        ]
