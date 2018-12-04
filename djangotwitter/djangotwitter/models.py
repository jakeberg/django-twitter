from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Post(models.Model):
    body = models.TextField(max_length=150)
    likes = models.Integer()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


    def __str__(self):
        return self.title