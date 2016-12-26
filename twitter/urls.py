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
from post.views import basic_one,template_two, template_three_simple, posts, addlike

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^basicview/1', basic_one),
    url(r'^basicview/2', template_two),
    url(r'^basicview/3', template_three_simple),
    url(r'^posts/all/$', post.views.posts),
    url(r'^posts/addlike/(?P<post_id>\d+)/$', post.views.addlike),
    url(r'^posts/addlike/', post.views.addlike),
    url(r'^', posts),

]
