from django.db import models

from user_control.constants import BLOOD_GROUP_CHOICES, GENDER_CHOICES, STATUS_CHOICES
from user_control.models import UserModel


class CovidTestModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    date = models.DateField()
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True
    )
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.patient_name

    class Meta:
        verbose_name = "Covid Test"
        verbose_name_plural = "Covid Tests"
