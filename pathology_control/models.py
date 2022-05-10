from django.db import models
from user_control.constants import *
from user_control.models import UserModel


class TestTypeModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Test Type"
        verbose_name_plural = "Test Types"


class TestModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    test_type = models.ForeignKey(TestTypeModel, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    date = models.DateField()
    patient_name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True
    )
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES, null=True, blank=True
    )
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Pathology Test"
        verbose_name_plural = "Pathology Tests"
