from django.db import models
from user_control.constants import *
from user_control.models import PatientModel


class OTScheduleModel(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "OT Schedule"
        verbose_name_plural = "OT Schedules"
