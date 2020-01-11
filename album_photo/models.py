from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Photo(models.Model):
    path = models.ImageField()
    creation_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="like_pictures")





