from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from djangotwitter.models import Author, Post
from djangotwitter.forms import LoginForm, SignupForm, PostForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


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
            Author.objects.create(name=user.username, user=user, bio="")
            return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})


def login_view(request):

    html = "login.html"

    form = LoginForm(None or request.POST)
 
    if form.is_valid():
        next = request.POST.get('next')
        data = form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        
        if user is not None:
            login(request, user)  
        if next:
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect("/")

    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required()
def homepage_view(request):

    html = "homepage.html"
    current_user = Author.objects.filter(user=request.user).first()
    content = {
        "posts": Post.objects.filter(author__id=current_user.id).order_by('date').reverse(),
        "following": current_user.following.all()
    }

    return render(request, html, content)


@login_required()
def post_view(request):

    html = "post.html"

    if request.method == "POST":
        form = PostForm(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Post.objects.create(
                body=data['body'],
                author=Author.objects.filter(id=data['author']).first()
            )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = PostForm(user=request.user)

    return render(request, html, {"form": form})


def user_page_view(request, username):

    html = "user_page.html"

    user = Author.objects.filter(name=username).first()

    content = {
        'user': user,
        "posts": Post.objects.filter(author__id=user.id).order_by('date').reverse(),
        "following": user.following.all()
    }

    if request.method == "POST":
        current_user = Author.objects.filter(user=request.user).first()
        username = request.POST.get('username')
        author = Author.objects.filter(name=username).first()
        current_user.following.add(author.id)

    return render(request, html, content)


def error_view(request):

    html = "error.html"

    return render(request, html)
