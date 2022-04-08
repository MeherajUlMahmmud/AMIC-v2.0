from django.db import models
from user_control.models import UserModel


class CommunityPostModel(models.Model):
    """
    This is the model for a community post.
    This model has these attributes:
    author: the user who wrote the post
    title: the title of the post
    content: the content of the post
    image: the image of the post
    date_posted: the date the post was posted
    slug: the slug of the post
    totalViewCount: the total number of views of the post
    """
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    totalViewCount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " by " + self.author.name
