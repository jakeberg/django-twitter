from django.shortcuts import render
from djangotwitter.models import TwitterUser
from django.contrib.auth.decorators import login_required


@login_required()
def user_list_view(request):

    html = "user_list.html"
    authors = TwitterUser.objects.all()

    content = {
        "authors": authors,

    }

    return render(request, html, content)
