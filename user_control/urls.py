from django.urls import path

from .views import *


urlpatterns = [
    path('', home_view, name='home'),

    # user login, logout and registration url
    path('auth/login', login_view, name='login'),  # login
    path('auth/logout', logout_view, name='logout'),  # logout
    path('auth/doctor-registration', doctor_signup_view, name='doctor-register'),  # doctor registration
    path('auth/patient-registration', patient_signup_view, name='patient-register'),  # patient registration

    # doctor and patient feed url
    path('doctor-dashboard', doctor_dashboard, name='doctor-dashboard'),  # doctor dashboard
    path('patient-dashboard', patient_dashboard, name='patient-dashboard'),  # patient dashboard

    # doctor profile and patient profile
    path('doctor-profile/<str:pk>', doctor_profile_view, name='doctor-profile'),  # doctor profile
    path('patient-profile/<str:pk>', patient_profile_view, name='patient-profile'),  # patient profile

    # doctor and patient profile edit url
    path('update-doctor-profile', doctor_edit_profile, name='doctor-edit-profile'),  # doctor profile edit
    path('update-patient-profile',
         patient_edit_profile, name='patient-edit-profile'),  # patient profile edit

    # utilities
    path('auth/account-settings', account_settings_view, name='account-settings'),  # account settings
    path('contact-us', contact_view, name='contact'),  # contact page
]
