from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Photo(models.Model):
    path = models.ImageField()
    description = models.CharField(max_length = 500)
    creation_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="like_pictures")


class Comment(models.Model):
    content = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    photo = models.ManyToManyField(Photo, related_name="photo_comments")
    author = models.ManyToManyField(User, related_name="author_comments")
    active = models.BooleanField(default=True)

