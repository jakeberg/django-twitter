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
from djangotwitter import views
from djangotwitter.models import TwitterUser, Tweet
admin.site.register(TwitterUser)
admin.site.register(Tweet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', views.homepage_view, name='homepage'),
    path('error/', views.error_view, name='error'),
    path('login/', views.login_view),
    path('signup/', views.signup_view),
    path('logout/', views.logout_view),
    path('post/', views.post_view),
    path('author/<str:username>/', views.user_page_view),
    path('post/<int:id>/', views.tweet_view),
    path('delete/<int:id>/', views.delete_tweet_view)
]
