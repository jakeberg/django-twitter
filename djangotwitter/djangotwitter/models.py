from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Post(models.Model):
    body = models.TextField(max_length=150)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)


    def __str__(self):
        return self.body


class Following(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


    def __str__(self):
        return self.name