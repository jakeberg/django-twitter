from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from djangotwitter.models import TwitterUser
from djangotwitter.forms import LoginForm, SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def login_view(request):

    html = "login.html"

    form = LoginForm(None or request.POST)

    if form.is_valid():
        next = request.POST.get('next')
        data = form.cleaned_data
        user = authenticate(
            username=data['username'],
            password=data['password']
            )

        if user is not None:
            login(request, user)
        if next:
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect("/")

    return render(request, html, {'form': form})


def signup_view(request):

    html = "signup.html"

    form = SignupForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        if User.objects.filter(username=data['username']).exists():
            return HttpResponseRedirect(reverse('error'))
        else:
            user = User.objects.create_user(
                data['username'], data['email'], data['password'])
            login(request, user)
            TwitterUser.objects.create(name=user.username, user=user, bio="")
            return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})


def logout_view(request):

    logout(request)

    return HttpResponseRedirect(reverse('homepage'))
