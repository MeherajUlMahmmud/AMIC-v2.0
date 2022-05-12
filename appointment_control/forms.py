from django import forms
from .models import *
from django.forms import ModelForm


class PatientAppointmentForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = AppointmentModel
        fields = "__all__"
        exclude = [
            "patient",
            "doctor",
            "time",
            "meet_link",
            "department",
            "is_accepted",
            "is_canceled",
            "is_complete",
            "date_created",
        ]


class DoctorAppointmentForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    meet_link = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "https://meet.google.com/eig-xdgg-ixj"}
        )
    )

    class Meta:
        model = AppointmentModel
        fields = "__all__"
        exclude = [
            "patient",
            "doctor",
            "department",
            "is_accepted",
            "is_canceled",
            "is_complete",
            "date_created",
        ]


class PrescriptionForm(ModelForm):
    class Meta:
        model = PrescriptionModel
        fields = "__all__"
        exclude = ["appointment"]
