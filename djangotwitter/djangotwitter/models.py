from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class TwitterUser(models.Model):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=50)
    following = models.ManyToManyField("self", symmetrical=False, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Tweet(models.Model):
    body = models.TextField(max_length=150)
    author = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)


    def __str__(self):
        return self.body


class Notification(models.Model):
    tweet = models.OneToOneField(Tweet, on_delete=models.CASCADE)
    author = models.ForeignKey(TwitterUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.author.name

