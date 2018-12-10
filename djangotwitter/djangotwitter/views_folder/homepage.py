from django.shortcuts import render
from djangotwitter.models import TwitterUser, Tweet, Notification
from django.contrib.auth.decorators import login_required


@login_required()
def homepage_view(request):

    html = "homepage.html"
    current_author = TwitterUser.objects.filter(user=request.user).first()
    posts_followers = Tweet.objects.filter(
        author__in=list(current_author.following.all()))
    posts = Tweet.objects.filter(author__id=current_author.id)
    all_posts = posts.union(posts_followers).order_by('date').reverse()
    notifications = Notification.objects.filter(author__id=current_author.id)

    content = {
        "posts": all_posts,
        "following": current_author.following.all(),
        "number_of_following": len(current_author.following.all()),
        "number_of_posts": len(posts),
        "number_of_notifications": len(notifications),
        "current_author": current_author
    }

    return render(request, html, content)
