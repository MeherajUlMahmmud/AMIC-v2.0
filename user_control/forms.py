from django import forms
from django.contrib.auth.forms import UserCreationForm, authenticate
from django.forms import ModelForm
from user_control.constants import *
from .models import *


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Email Address"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    class Meta:
        model = UserModel
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get("email")
            password = self.cleaned_data.get("password")
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Username or Password")


class DoctorRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        help_text="Required. Add a valid email address",
        widget=forms.TextInput(attrs={"placeholder": "Email Address"}),
    )
    name = forms.CharField(
        max_length=60, widget=forms.TextInput(attrs={"placeholder": "Full Name"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        help_text="Password must contain at least 8 character including numeric values",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
        help_text="Re-type Password",
    )
    check = forms.BooleanField(required=True)

    class Meta:
        model = UserModel
        fields = ("name", "email", "password1", "password2", "check")


class PatientRegistrationForm(UserCreationForm):

    email = forms.EmailField(
        max_length=255,
        help_text="Required. Add a valid email address",
        widget=forms.TextInput(attrs={"placeholder": "Email Address"}),
    )
    name = forms.CharField(
        max_length=60, widget=forms.TextInput(attrs={"placeholder": "Full Name"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        help_text="Password must contain at least 8 character including numeric values",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
        help_text="Re-type Password",
    )
    check = forms.BooleanField(required=True)

    class Meta:
        model = UserModel
        fields = ("name", "email", "password1", "password2", "check")


class DoctorEditProfileForm(ModelForm):
    image = forms.ImageField(
        required=False,
        error_messages={"invalid": "Image files only"},
        widget=forms.FileInput,
    )
    gender = forms.CharField(widget=forms.Select(choices=GENDER_CHOICES))
    blood_group = forms.CharField(widget=forms.Select(choices=BLOOD_GROUP_CHOICES))
    date_of_birth = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    last_donation = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = DoctorModel
        fields = "__all__"
        exclude = ["user", "created_at", "updated_at"]


class PatientEditProfileForm(ModelForm):
    image = forms.ImageField(
        required=False,
        error_messages={"invalid": "Image files only"},
        widget=forms.FileInput,
    )
    gender = forms.CharField(widget=forms.Select(choices=GENDER_CHOICES))
    blood_group = forms.CharField(widget=forms.Select(choices=BLOOD_GROUP_CHOICES))
    date_of_birth = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )
    last_donation = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = PatientModel
        fields = "__all__"
        exclude = ["user", "created_at", "updated_at"]


class AccountInformationForm(ModelForm):
    name = forms.CharField(
        max_length=60, widget=forms.TextInput(attrs={"placeholder": "Full Name"})
    )
    email = forms.EmailField(
        max_length=255,
        help_text="Required. Add a valid email address",
        widget=forms.TextInput(attrs={"placeholder": "Email Address"}),
    )

    class Meta:
        model = UserModel
        fields = ("name", "email")
