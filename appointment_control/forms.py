from django import forms
from .models import *
from django.forms import ModelForm


class PatientAppointmentForm(ModelForm):
    """
    This is the form that will be used to create a new appointment by a patient.
    This form will display a input field for the patient's name, a input field for the patient's phone number,
    a date input field, and a textfield to enter the reason for the appointment.
    """
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = AppointmentModel
        fields = '__all__'
        exclude = ['patient', 'doctor', 'time', 'meet_link', 'department', 'is_accepted', 'is_canceled', 'is_complete',
                   'date_created']


class DoctorAppointmentForm(ModelForm):
    """
    This is the form that will be used to accept a appointment by a doctor.
    While accepting the doctor will insert some data into the form i.e. the appointment's time, the google meet link, and the doctor can change the date of appointment.
    """
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    meet_link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'https://meet.google.com/eig-xdgg-ixj'}))

    class Meta:
        model = AppointmentModel
        fields = '__all__'
        exclude = ['patient', 'doctor', 'department', 'is_accepted', 'is_canceled', 'is_complete',
                   'date_created']


class PrescriptionForm(ModelForm):
    """
    This is the form to write a prescription for a patient.
    This form will display a textfield for entering the prescription details.
    """
    class Meta:
        model = PrescriptionModel
        fields = '__all__'
        exclude = ['appointment']
