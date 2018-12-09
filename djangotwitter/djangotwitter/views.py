from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from djangotwitter.models import TwitterUser, Tweet, Notification
from djangotwitter.forms import LoginForm, SignupForm, TweetForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import re

@login_required()
def homepage_view(request):

    html = "homepage.html"
    current_author = TwitterUser.objects.filter(user=request.user).first()
    posts_followers = Tweet.objects.filter(author__in=list(current_author.following.all()))
    posts = Tweet.objects.filter(author__id=current_author.id)
    all_posts = posts.union(posts_followers).order_by('date').reverse()
    notifications = Notification.objects.filter(author__id=current_author.id)

    content = {
        "posts": all_posts,
        "following": current_author.following.all(),
        "number_of_following": len(current_author.following.all()),
        "number_of_posts": len(posts),
        "number_of_notifications": len(notifications),
    }

    return render(request, html, content)


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
                        author=TwitterUser.objects.filter(name=match[1:]).first()
                    )

            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = TweetForm(user=request.user)

    return render(request, html, {"form": form})


def user_page_view(request, username):

    html = "user_page.html"

    author = TwitterUser.objects.filter(name=username).first()
    posts = Tweet.objects.filter(
        author__id=author.id).order_by('date').reverse()
    following = author.following.all()
    current_user_follows = TwitterUser.objects.filter(user=request.user).first().following.all()

    content = {
        "user": author,
        "posts": posts,
        "following": following,
        "number_of_following": len(following),
        "number_of_posts": len(posts),
        "already_following": True if author in current_user_follows else False,
        "is_self": True if author.user == request.user else False
    }

    if request.method == "POST":
        rule = request.POST.get('rule')
        current_author = TwitterUser.objects.filter(user=request.user).first()
        username = request.POST.get('username')
        author = TwitterUser.objects.filter(name=username).first()
        if rule == "follow":
            current_author.following.add(author.id)
        elif rule == "unfollow":
            current_author.following.remove(author.id)
        return HttpResponseRedirect('/author/' + author.name)

    return render(request, html, content)


def tweet_view(request, id):

    html = "tweet.html"

    tweet = Tweet.objects.get(id=id)

    content = {
        "tweet": tweet
    }

    return render(request, html, content)


def delete_tweet_view(request, id):

    html = "tweet.html"

    Tweet.objects.filter(id=id).delete()

    return HttpResponseRedirect(reverse('homepage'))


def notification_view(request):

    html = "notifications.html"

    current_author = TwitterUser.objects.filter(user=request.user).first()
    notifications = Notification.objects.filter(author__id=current_author.id)
    tweet_ids = [i.tweet_id for i in notifications]
    tweets = Tweet.objects.filter(id__in=list(tweet_ids))


    content = {
        "tweets": tweets
    }

    return render(request, html, content)

def delete_notifications_view(request):

    current_author = TwitterUser.objects.filter(user=request.user).first()
    notifications = Notification.objects.filter(author__id=current_author.id).delete()

    return HttpResponseRedirect(reverse('homepage'))


def error_view(request):

    html = "error.html"

    return render(request, html)
