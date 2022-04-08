from django.urls import path

from .views import *

urlpatterns = [
    path('', article_home_view, name='article-home'),

    path('post', post_article_view, name='post-article'),
    path('<str:slug>/', article_details_view, name='article-details'),
    path('edit/<str:slug>/', edit_article_view, name='edit-article'),
    path('delete/<str:slug>/', delete_article_view, name='delete-article'),

    path('user/<str:pk>/', users_articles_view, name='users-articles'),
    path('category/<str:cat>/', category_articles_view, name='category-articles'),
]
