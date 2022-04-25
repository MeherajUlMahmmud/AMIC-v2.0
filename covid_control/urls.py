from django.urls import path

from .views import *

urlpatterns = [
    path("", covid_home_view, name="covid-home"),  # path for home page
    path("book", covid_post_view, name="covid-post"),  # path for post request
    path(
        "covid-test-update/<int:pk>",
        covid_update_view,
        name="covid-update",
    ),  # path for update request
    path(
        "covid-test-delete/<int:pk>",
        covid_delete_view,
        name="covid-delete",
    ),  # path for delete request
    path(
        "covid-test-detail/<int:pk>",
        covid_detail_view,
        name="covid-detail",
    ),  # path for request detail
]
