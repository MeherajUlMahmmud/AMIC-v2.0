from django.db import models

from user_control.models import UserModel


class AdviceModel(models.Model):
    """
    This class represents the Advice model.
    This class is responsible for creating the data model for the Advice model.

    Attributes:
        author: The user who created the advice.
        title: The title of the advice.
        content: The description of the advice.
        image: The image of the advice.
        date_posted: The date and time when the advice was created.
        slug: The unique identifier of the advice.
        totalViewCount: The total number of views of the advice.
    """
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="images/advisor/", null=True, blank=True)
    slug = models.SlugField(unique=True)
    totalViewCount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " by " + self.author.name

    class Meta:
        verbose_name = 'Advice'
        verbose_name_plural = 'Advices'
