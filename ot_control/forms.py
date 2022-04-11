from .models import *
from django.forms import ModelForm
from django import forms


class OTScheduleForm(ModelForm):
	"""
	This form is used to create a new OT Schedule.
	"""
	class Meta:
		model = OTScheduleModel
		fields = "__all__"
		exclude = ['patient', 'status', 'created_at', 'updated_at']
