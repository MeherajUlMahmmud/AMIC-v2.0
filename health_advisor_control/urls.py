from django.urls import path

from .views import *

urlpatterns = [
    path('', advisor_home_view, name='advisor-home'),
    path('post/new/', advisor_post_create_view, name='advisor-post-create'),
    path('post/<str:slug>/', advisor_post_detail_view, name='advisor-post-detail'),
    path('post/update/<str:slug>/', advisor_post_update_view, name='advisor-post-update'),
    path('post/delete/<str:slug>/', advisor_post_delete_view, name='advisor-post-delete'),
]
