from datetime import date
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from .constants import *


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Must have an email address")

        if not name:
            raise ValueError("Must have a name")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class PatientModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/users/", null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True
    )
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES, null=True, blank=True
    )
    height = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(max_length=100, null=True, blank=True)
    last_donation = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name

    def calc_bmi(self):
        return round(self.weight / (self.height**2), 2)

    def calc_age(self):
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"


class SpecializationModel(models.Model):
    specialization = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.specialization

    class Meta:
        verbose_name = "Specialization"
        verbose_name_plural = "Specializations"


class DoctorModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images/users/", null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    NID = models.CharField(max_length=50, null=True, blank=True)
    specialization = models.ForeignKey(
        SpecializationModel, null=True, blank=True, on_delete=models.SET_NULL
    )
    BMDC_regNo = models.CharField(max_length=100, null=True, blank=True)
    last_donation = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name

    def calc_age(self):
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


class FeedbackModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.email

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
