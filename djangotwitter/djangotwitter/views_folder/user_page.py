from django.shortcuts import render
from django.http import HttpResponseRedirect
from djangotwitter.models import TwitterUser, Tweet


def user_page_view(request, user_id):

    html = "user_page.html"

    author = TwitterUser.objects.filter(id=user_id).first()
    posts = Tweet.objects.filter(
        author__id=author.id).order_by('date').reverse()
    following = author.following.all()
    current_user_follows = TwitterUser.objects.filter(
        user=request.user).first().following.all()

    content = {
        "author": author,
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
        author_id = request.POST.get('id')
        author = TwitterUser.objects.filter(id=author_id).first()
        if rule == "follow":
            current_author.following.add(author.id)
        elif rule == "unfollow":
            current_author.following.remove(author.id)
        return HttpResponseRedirect('/author/' + str(author.id))

    return render(request, html, content)
