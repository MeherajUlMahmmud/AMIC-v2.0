from django.urls import path

from .views import *

urlpatterns = [
    path('', pharmacy_home_view, name='pharmacy-home'),
]
