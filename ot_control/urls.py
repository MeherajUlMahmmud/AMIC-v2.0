from django.urls import path

from .views import *

urlpatterns = [
    path('', ot_booking_home_view, name='ot-booking-home'), # path for home page
    path('book', ot_booking_post_view, name='ot-booking-post'), # path for post request
    path('update-booking/<int:pk>', update_ot_bookng_view, name='ot-booking-update'), # path for update request
    path('delete-booking/<int:pk>', delete_ot_booking_view, name='ot-booking-delete'), # path for delete request
    path('booking-detail/<int:pk>', ot_booking_detail_view, name='ot-booking-detail'), # path for request detail
    path('bookings/<int:pk>', users_ot_booking_view, name='users-ot-booking'), # path for user requests

]
