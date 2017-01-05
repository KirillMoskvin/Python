"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
import post
from post.views import posts, addlike, addpost
from loginsys.views import login, logout, register
from post.views import indexusers, getuserwall, init_profiles, reset_likes, add_subscribe, feed

urlpatterns = [
    url(r'^auth/login', login),
    url(r'^auth/logout/', logout),
    url(r'^auth/register/', register),
    url(r'^admin/', admin.site.urls),

    url(r'^posts/all/$', post.views.posts),
    url(r'^posts/addlike/(?P<post_id>\d+)/$', post.views.addlike),
    url(r'^add_subscribe/(?P<user_id>\d+)/$', add_subscribe),
    url(r'^posts/addlike/', post.views.addlike),
    url(r'^posts/addpost/', addpost),
    url(r'^users/all/', indexusers),
    url(r'^user/(?P<user_id>\d+)/$', getuserwall),
    url(r'^feed/', feed),

    url(r'^init_profiles/', init_profiles), #######################
    url(r'^reset_likes/', reset_likes),  #######################


    url(r'^', posts),
]