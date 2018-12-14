"""djangotwitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from djangotwitter.views_folder import (
    auth, homepage, post, user_page, tweet, notification, error, user_list)
from djangotwitter.models import TwitterUser, Tweet, Notification
admin.site.register(TwitterUser)
admin.site.register(Tweet)
admin.site.register(Notification)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', homepage.homepage_view, name='homepage'),
    path('error/', error.error_view, name='error'),
    path('login/', auth.login_view),
    path('signup/', auth.signup_view),
    path('logout/', auth.logout_view),
    path('post/', post.post_view),
    path('user_list/', user_list.user_list_view),
    path('author/<int:user_id>/', user_page.user_page_view),
    path('post/<int:id>/', tweet.tweet_view),
    path('delete/<int:id>/', tweet.delete_tweet_view),
    path('notifications/', notification.notification_view),
]
