from django.urls import path

from .views import *

urlpatterns = [
    path("", pathology_home_view, name="pathology-home"),  # path for home page
    path("book", pathology_post_view, name="pathology-post"),  # path for post request
    path(
        "update-booking/<int:pk>",
        update_pathology_view,
        name="pathology-update",
    ),  # path for update request
    path(
        "delete-booking/<int:pk>",
        delete_pathology_view,
        name="pathology-delete",
    ),  # path for delete request
    path(
        "booking-detail/<int:pk>",
        pathology_detail_view,
        name="pathology-detail",
    ),  # path for request detail
]
