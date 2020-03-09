from django.contrib.auth.models import User
from django.db import models


class Photo(models.Model):
    path = models.ImageField()
    description = models.CharField(max_length = 500)
    creation_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="like_pictures")

    def __str__(self):
        return f"{self.description}"


class Comment(models.Model):
    content = models.CharField(max_length=500)
    creation_date = models.DateTimeField(auto_now_add=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.content}"
