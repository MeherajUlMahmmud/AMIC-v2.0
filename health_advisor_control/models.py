from django.db import models

from user_control.models import UserModel


class AdviceModel(models.Model):
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
