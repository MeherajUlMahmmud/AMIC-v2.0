from datetime import date
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


# User manager for the User Model
class MyUserManager(BaseUserManager):
    """
    This is a custom manager for the Custom User model.
    """
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Must have an email address')

        if not name:
            raise ValueError('Must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
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


# User Model (Common for all the users)
class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    This is the Custom User model.
    This is the model that will be used to create the users in the system.
    This model includes the following fields:
    email: The email address of the user.
    name: The name of the user.
    is_active: A boolean field that specifies whether the user is active or not.
    is_staff: A boolean field that specifies whether the user is a staff member or not.
    is_admin: A boolean field that specifies whether the user is an admin or not.
    date_joined: A date field that specifies when the user joined the system.
    """
    email = models.EmailField(max_length=255, unique=True)  # Email
    name = models.CharField(max_length=255)  # Name
    is_patient = models.BooleanField(default=False)  # True if patient
    is_doctor = models.BooleanField(default=False)  # True if doctor
    is_active = models.BooleanField(default=True)  # True if active
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Email & Password are required by default.

    objects = MyUserManager()  # User manager for the User Model

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# Patient Model (Only for Patients / Patients' Profile)
class PatientModel(models.Model):
    """
    This is the model that will be used to create the patient's profile.
    This model includes the following fields:
    user: A one-to-one field that references the User model.
    image: A file field that stores the patient's image.
    gender: The gender of the patient.
    blood_group: The blood group of the patient
    height: The height of the patient in inches.
    weight: The weight of the patient in pounds.
    date_of_birth: The date of birth of the patient.
    phone: The phone number of the patient.
    address: The address of the patient.
    last_donation: The date of the last blood donation of the patient.
    """

    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('', 'Select Blood Group'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/users/", null=True, blank=True)  # Patient Profile Picture
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
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
        return round(self.weight / (self.height ** 2), 2)

    def calc_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


"""
Specialization Model for Doctors in order to make the 
specialization field in Doctor Profile dynamic
"""


class SpecializationModel(models.Model):
    specialization = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.specialization

    class Meta:
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'


# Doctor Model (only for Doctors / Doctors' Profile)
class DoctorModel(models.Model):
    """
    This is the model that will be used to create the doctor's profile.
    This model includes the following fields:
    user: A one-to-one field that references the User model.
    bio: A text field that stores the doctor's bio.
    image: A file field that stores the doctor's image.
    gender: The gender of the patient.
    blood_group: The blood group of the doctor
    date_of_birth: The date of birth of the doctor.
    phone: The phone number of the doctor.
    nid: The national id card number of the doctor.
    specialization: The specialization of the doctor.
    bmdc_reg_no: The BMDC registration number of the doctor.
    last_donation: The date of the last blood donation of the doctor.

    """

    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('', 'Select Blood Group'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images/users/", null=True, blank=True) # Doctor Profile Picture
    gender = models.CharField(max_length=10, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    NID = models.CharField(max_length=50, null=True, blank=True)
    specialization = models.ForeignKey(SpecializationModel, null=True, blank=True, on_delete=models.SET_NULL)
    BMDC_regNo = models.CharField(max_length=100, null=True, blank=True)
    last_donation = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name

    def calc_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'


# Responses from Contact Us form will be saved here
class FeedbackModel(models.Model):
    """
    This is the model that will be used to store the feedback data.
    This model includes the following fields:
    name: The name of the user.
    email: The email of the user.
    subject: The subject of the feedback.
    message: The message of the feedback.
    """
    name = models.CharField(max_length=255)  # name of the user
    email = models.CharField(max_length=255)  # email of the user
    subject = models.CharField(max_length=255)  # subject of the message
    message = models.TextField()  # message body
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.email

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
