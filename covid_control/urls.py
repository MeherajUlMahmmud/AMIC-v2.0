from django.urls import path

from .views import *

urlpatterns = [
    path("", covid_home_view, name="covid-home"),
    path("book-test", covid_post_view, name="covid-post"),
    path(
        "covid-test-update/<int:pk>",
        covid_update_view,
        name="covid-update",
    ),
    path(
        "covid-test-delete/<int:pk>",
        covid_delete_view,
        name="covid-delete",
    ),
    path(
        "covid-test-detail/<int:pk>",
        covid_detail_view,
        name="covid-detail",
    ),
]
