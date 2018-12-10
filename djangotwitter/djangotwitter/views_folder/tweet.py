from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from djangotwitter.models import Tweet


def tweet_view(request, id):

    html = "tweet.html"

    tweet = Tweet.objects.get(id=id)

    content = {
        "tweet": tweet
    }

    return render(request, html, content)


def delete_tweet_view(request, id):

    Tweet.objects.filter(id=id).delete()

    return HttpResponseRedirect(reverse('homepage'))
