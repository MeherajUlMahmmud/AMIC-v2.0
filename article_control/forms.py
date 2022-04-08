from django import forms
from .models import *
from django.forms import ModelForm


class ArticleForm(ModelForm):
    """
    This is the form that will be used to create and edit articles.
    This form will show the article title, subtitle, catgeory, the article content, and the article image field.
    """
    image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)

    class Meta:
        model = ArticleModel
        fields = '__all__'
        exclude = ['author', 'slug', 'totalViewCount']
