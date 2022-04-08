from django import forms

from .models import CommunityPostModel


class AddEditPostForm(forms.ModelForm):
    """
    This form is used to add or edit a patient community post.

    This form contains a 'title' field and a 'content' field, along with a 'image' field.
     - title: The title of the post.
     - content: The content of the post.
     - image: The image of the post (optional).
    """
    image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"},
                             widget=forms.FileInput)

    class Meta:
        model = CommunityPostModel
        fields = ['title', 'content', 'image']
