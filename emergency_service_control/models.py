from django.db import models

from user_control.models import UserModel


class BloodRequestModel(models.Model):
    """
    This class represents the model for a request for blood.
    The user who requested the blood is the foreign key.
    This model has the following attributes:
    user: The user who requested the blood.
    patient_name: The name of the patient.
    gender: The gender of the patient
    blood_group: The blood group of the user.
    quantity: The unit of blood needed.
    location: The location where the patient is staying
    is_emergency: A boolean field that specifies whether the request is emergency or not.
    is_active: A boolean field that specifies whether the user is active or not.
    needed_within: The time when the blood is needed.
    phone: The phone number of the user.
    note: The note of the user.
    posted_on: The time when the request was posted.
    """
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE) # user who requested blood
    patient_name = models.CharField(max_length=100) # patient's name
    gender = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=255)
    quantity = models.IntegerField() # quantity of blood requested
    location = models.TextField(max_length=255)
    is_emergency = models.BooleanField(default=False) # is this request for an emergency
    is_active = models.BooleanField(default=True) # is this request active
    needed_within = models.DateField() # when is the blood needed
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blood_group, "Blood requested by", self.user.name


class PlasmaRequestModel(models.Model):
    """
    This class represents the model for a request for plasma.
    The user who requested the plasma is the foreign key.
    This model has the following attributes:
    user: The user who requested the plasma.
    patient_name: The name of the patient.
    gender: The gender of the patient
    blood_group: The blood group of the user.
    quantity: The unit of plasma needed.
    location: The location where the patient is staying
    is_emergency: A boolean field that specifies whether the request is emergency or not.
    is_active: A boolean field that specifies whether the user is active or not.
    needed_within: The time when the plasma is needed.
    phone: The phone number of the user.
    note: The note of the user.
    posted_on: The time when the request was posted.
    """
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.TextField(max_length=255)
    is_emergency = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    needed_within = models.DateField()
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blood_group, "Plasma requested by", self.user.name
