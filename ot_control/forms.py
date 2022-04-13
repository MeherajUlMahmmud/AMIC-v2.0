from .models import *
from django.forms import ModelForm
from django import forms


class OTScheduleForm(ModelForm):
	"""
	This form is used to create a new OT Schedule.
	"""
	start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
	end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
	date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
	
	class Meta:
		model = OTScheduleModel
		fields = "__all__"
		exclude = ['patient', 'status', 'created_at', 'updated_at']
