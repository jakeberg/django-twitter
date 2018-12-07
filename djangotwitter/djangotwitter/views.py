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
    current_author = Author.objects.filter(user=request.user).first()
    posts = Post.objects.filter(author__id=current_author.id).order_by('date').reverse()

    content = {
        "posts": posts,
        "following": current_author.following.all(),
        "number_of_following": len(current_author.following.all()),
        "number_of_posts": len(posts)
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

    author = Author.objects.filter(name=username).first()
    posts = Post.objects.filter(author__id=author.id).order_by('date').reverse()
    following = author.following.all()
    current_user_follows = Author.objects.filter(user=request.user).first().following.all()

    content = {
        'user': author,
        "posts": posts,
        "following": following,
        "number_of_following": len(following),
        "number_of_posts": len(posts),
        "already_following": True if author in current_user_follows else False,
        "is_self": True if author.user == request.user else False
    }

    if request.method == "POST":
        rule = request.POST.get('rule')
        if rule == "follow":
            current_author = Author.objects.filter(user=request.user).first()
            username = request.POST.get('username')
            author = Author.objects.filter(name=username).first()
            current_author.following.add(author.id)
        elif rule == "unfollow":
            current_author = Author.objects.filter(user=request.user).first()
            username = request.POST.get('username')
            author = Author.objects.filter(name=username).first()
            current_author.following.remove(author.id)
        return HttpResponseRedirect('/author/' + author.name)

    return render(request, html, content)


def tweet_view(request, id):

    html = "tweet.html"

    tweet = Post.objects.get(id=id)

    content = {
        "tweet": tweet
    }

    return render(request, html, content)


def delete_tweet_view(request, id):

    html = "tweet.html"

    Post.objects.filter(id=id).delete()

    return HttpResponseRedirect(reverse('homepage'))


def error_view(request):

    html = "error.html"

    return render(request, html)
