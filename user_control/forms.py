from django import forms
from django.contrib.auth.forms import UserCreationForm, authenticate
from django.forms import ModelForm

from .models import *


class LoginForm(forms.Form):  # LoginForm
    """
    This form is used to login a user.

    This form displays an email, and a password field.
    """
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))  # email
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))  # password

    class Meta:
        model = UserModel
        fields = ('email', 'password')

    def clean(self):  # clean
        if self.is_valid():
            email = self.cleaned_data.get('email')  # get cleaned email
            password = self.cleaned_data.get('password')  # get cleaned password
            if not authenticate(email=email, password=password):  # if email and password are not valid
                raise forms.ValidationError("Invalid Username or Password")  # raise error


class DoctorRegistrationForm(UserCreationForm):
    """
    This form is used to register a doctor.

    This form displays an email, a name, a password, and a confirm password field.
    """
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address',
                             widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text='Password must contain at least 8 character including numeric values',
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        help_text='Re-type Password',
    )
    check = forms.BooleanField(required=True)

    class Meta:
        model = UserModel
        fields = ("name", "email", "password1", "password2", "check")


class PatientRegistrationForm(UserCreationForm):
    """
    This form is used to register a patient.

    This form displays an email, a name, a password, and a confirm password field.
    """
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address',
                             widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text='Password must contain at least 8 character including numeric values',
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        help_text='Re-type Password',
    )
    check = forms.BooleanField(required=True)

    class Meta:
        model = UserModel  # UserModel
        fields = ("name", "email", "password1", "password2", "check")  # fields


class DoctorEditProfileForm(ModelForm):
    """
    This form is used to edit a doctor's profile.

    This form displays
     - specialization: a dropdown list of all the specializations
     - profile_pic: a file input for the doctor's profile picture
     - bio: a textarea for the doctor's bio
     - blood_group: a drop down for doctor's blood group
     - date_of_birth: a date input for the doctor's date of birth
     - nid: a text input for the doctor's NID
     - bmdc_reg_no: a text input for the doctor's BMDC registration number
     - gender: a drop down for doctor's gender
     - last_donation: a date input for the doctor's last donation
    """
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
    )  # image
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))  # date of birth
    last_donation = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))  # last donation

    class Meta:
        model = DoctorModel  # get model
        fields = '__all__'  # get all fields
        exclude = ['user']  # Exclude the user field


class PatientEditProfileForm(ModelForm):
    """
    This form is used to edit a patient's profile.

    This form displays
     - profile_pic: a file input for the patient's profile picture
     - date_of_birth: a date input for the patient's date of birth
     - height: a text input for the patient's height
     - weight: a text input for the patient's weight
     - blood_group: a drop down for patient's blood group
     - gender: a drop down for patient's gender
     - last_donation: a date input for the patient's last donation
    """
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
    )  # image
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))  # date of birth
    last_donation = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))  # last donation

    class Meta:
        model = PatientModel  # PatientModel
        fields = '__all__'  # all fields
        exclude = ['user']  # exclude user


class AccountInformationForm(ModelForm):  # AccountInformationForm
    """
    This form is used to edit a user's account information.

    This form displays
     - email: a text input for the user's email
     - name: a text input for the user's name
    """
    name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))  # name
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address',
                             widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))  # email

    class Meta:
        model = UserModel  # model
        fields = ('name', 'email')  # fields
