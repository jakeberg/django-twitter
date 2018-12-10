from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from djangotwitter.models import TwitterUser, Tweet, Notification
from djangotwitter.forms import TweetForm
from django.contrib.auth.decorators import login_required
import re


@login_required()
def post_view(request):

    html = "post.html"

    if request.method == "POST":
        form = TweetForm(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            tweet = Tweet.objects.create(
                body=data['body'],
                author=TwitterUser.objects.filter(id=data['author']).first()
                )
            if "@" in data['body']:
                matches = re.findall(r'@\w+', data['body'])
                for match in matches:
                    Notification.objects.create(
                        tweet=Tweet.objects.get(id=tweet.id),
                        author=TwitterUser.objects.filter(
                            name=match[1:]).first()
                    )

            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = TweetForm(user=request.user)

    return render(request, html, {"form": form})
