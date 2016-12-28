from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect,render
from django.template import Context
from django.template.loader import get_template
from django.template.context_processors import csrf
from django.contrib import auth


from post.forms import PostForm
from post.models import Post

import datetime
# Create your views here.

def auth_required(function):
    def check_auth(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/auth/login/')
        return function(request)
    return check_auth

def posts(request):
    args = {'posts': Post.objects.all().order_by('-post_date'), 'post_form': PostForm,
            'user': auth.get_user(request)}
    args.update(csrf(request))
    return render_to_response('posts.html', args)


def posts_of_user(request, user_id):
    return render_to_response('posts.html', {'posts': Post.objects.filter(post_id=user_id)})


def addlike(request, post_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/auth/login/')
    try:
        post = Post.objects.get(id=post_id)
        post.post_likes += 1
        post.save()
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')


@auth_required
def addpost(request):
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_date=datetime.datetime.now()
            form.save()
    return redirect('/posts')


