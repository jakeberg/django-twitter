from django.shortcuts import render
from djangotwitter.models import TwitterUser, Tweet, Notification


def notification_view(request):

    html = "notifications.html"

    current_author = TwitterUser.objects.filter(user=request.user).first()
    notifications = Notification.objects.filter(author__id=current_author.id)
    tweet_ids = [i.tweet_id for i in notifications]
    tweets = Tweet.objects.filter(id__in=list(tweet_ids))

    content = {
        "tweets": tweets
    }

    Notification.objects.filter(author__id=current_author.id).delete()

    return render(request, html, content)
