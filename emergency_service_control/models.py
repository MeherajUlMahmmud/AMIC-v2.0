from django.db import models

from user_control.constants import *
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

    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE
    )  # user who requested blood
    patient_name = models.CharField(max_length=100)  # patient's name
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True
    )
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES, null=True, blank=True
    )
    quantity = models.IntegerField()  # quantity of blood requested
    location = models.TextField(max_length=255)
    is_emergency = models.BooleanField(
        default=False
    )  # is this request for an emergency
    is_active = models.BooleanField(default=True)  # is this request active
    needed_within = models.DateField()  # when is the blood needed
    phone = models.CharField(max_length=20)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blood_group, "Blood requested by", self.user.name

    class Meta:
        verbose_name = "Blood Request"
        verbose_name_plural = "Blood Requests"


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
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True
    )
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES, null=True, blank=True
    )
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

    class Meta:
        verbose_name = "Plasma Request"
        verbose_name_plural = "Plasma Requests"


class AmbulanceModel(models.Model):
    vehicle_number = models.CharField(max_length=30, unique=True)
    city = models.CharField(max_length=30, choices=CITY_CHOICES)
    type = models.CharField(max_length=20, choices=TYPES_CHOICES)
    driver_name = models.CharField(max_length=30, null=True, blank=True)
    driver_phone = models.CharField(max_length=20, null=True, blank=True)
    driver_email = models.EmailField(max_length=40, null=True, blank=True)
    driver_address = models.TextField(null=True, blank=True)
    driver_NID = models.CharField(max_length=25, null=True, blank=True, unique=True)
    driver_license = models.CharField(max_length=25, null=True, blank=True, unique=True)
    driver_gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True
    )
    driver_image = models.ImageField(
        upload_to="images/ambulance/", null=True, blank=True
    )
    ambulance_image = models.ImageField(null=True, blank=True)
    rent_inter_city = models.DecimalField(max_digits=10, decimal_places=2)
    rent_intra_civision = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehicle_number + " " + self.city

    class Meta:
        verbose_name = "Ambulance"
        verbose_name_plural = "Ambulances"
