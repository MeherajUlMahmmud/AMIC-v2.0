from django.urls import path

from .views import *

urlpatterns = [
    path('blood-donation', blood_donation_home_view, name='blood-donation-home'), # path for home page
    path('blood-donation/post-request', post_blood_request_view, name='blood-donation-post-request'), # path for post request
    path('blood-donation/update-request/<int:pk>', update_blood_request_view, name='blood-donation-update-request'), # path for update request
    path('blood-donation/delete-request/<int:pk>', delete_blood_request_view, name='blood-donation-delete-request'), # path for delete request
    path('blood-donation/request-detail/<int:pk>', blood_request_detail_view, name='blood-donation-request-detail'), # path for request detail
    path('blood-donation/requests/<int:pk>', users_requests_view, name='users-requests'), # path for user requests


	
    path('plasma-donation', plasma_donation_home_view, name='plasma-donation-home'),
    path('plasma-donation/post-request', post_plasma_request_view, name='plasma-donation-post-request'),
    path('plasma-donation/update-request/<int:pk>', update_plasma_request_view, name='plasma-donation-update-request'),
    path('plasma-donation/delete-request/<int:pk>', delete_plasma_request_view, name='plasma-donation-delete-request'),
    path('plasma-donation/request-detail/<int:pk>', plasma_request_detail_view, name='plasma-donation-request-detail'),
    path('plasma-donation/requests/<int:pk>', users_requests_view, name='users-plasma-requests'),
]
