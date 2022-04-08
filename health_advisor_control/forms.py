from django import forms
from django.forms import widgets
from .models import AdviceModel


class AddEditPostForm(forms.ModelForm):
    """
    This form is used to add or edit a health advice.

    This form displays a textarea for the user to enter a health advice, along with a title, and an image.
    """
    image = forms.ImageField(required=False,
                             error_messages={
                                 "required": "Please upload an image"},
                             widget=forms.FileInput)

    class Meta:
        model = AdviceModel
        fields = ['title', 'content', 'image']
