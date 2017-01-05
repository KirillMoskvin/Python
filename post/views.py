from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, render
from django.template import Context
from django.template.loader import get_template
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User

from post.forms import PostForm
from post.models import Post, Profile

import datetime


# Create your views here.

def auth_required(function):
    def check_auth(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/auth/login/')
        return function(request, *args, **kwargs)

    return check_auth


def posts(request):
    args = {'posts': Post.objects.all().order_by('-post_date'), 'post_form': PostForm,
            'user': auth.get_user(request), 'target_user': auth.get_user(request)}
    args.update(csrf(request))
    return render_to_response('posts.html', args)


def posts_of_user(request, user_id):
    return render_to_response('posts.html', {'posts': Post.objects.filter(post_id=user_id)})


def addlike(request, post_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/auth/login/')
    try:
        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(profile_user=auth.get_user(request))
        if post in profile.profile_likes.all():
            post.post_likes -= 1
            profile.profile_likes.remove(post)
            profile.save()
            post.save()
        else:
            post.post_likes += 1
            profile.profile_likes.add(post)
            post.save()
            profile.save()
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/user/' + str(Post.objects.get(id=post_id).post_author_id) + '/')


@auth_required
def addpost(request):
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.post_date = datetime.datetime.now()
            post.post_author_id = request.user.id
            form.save()
    return redirect('/posts')


def indexusers(request):
    args = {'users': User.objects.all(), 'user': auth.get_user(request)}
    return render_to_response('indexusers.html', args)


def getuserwall(request, user_id):
    try:
        args = {'target_user': User.objects.get(id=user_id), 'posts': Post.objects.all().order_by('-post_date'),
                'user': auth.get_user(request)}
        if args['target_user'].id == args['user'].id:
            args['post_form'] = PostForm()
        if Profile.objects.get(profile_user=args['target_user']) in Profile.objects.get(profile_user=args['user']).profile_subscribes.all():
            args['subscribed']=True
        else:
            args['subscribed']=False

        args.update(csrf(request))
        return render_to_response('posts.html', args)
    except ObjectDoesNotExist:
        raise Http404


# добавление подписки
@auth_required
def add_subscribe(request, user_id):
    try:
        user = auth.get_user(request)
        current_profile = Profile.objects.get(profile_user=user)
        if user_id != user.id:
            user_to_sub = Profile.objects.get(profile_user=User.objects.get(id=user_id))
            if user_to_sub in current_profile.profile_subscribes.all():
                current_profile.profile_subscribes.remove(user_to_sub)
            else:
                current_profile.profile_subscribes.add(user_to_sub)
            current_profile.save()
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/user/'+str(user_id)+'/')


# debug
def init_profiles(request):
    for user in User.objects.all():
        user_profile = Profile(profile_user=user)
        user_profile.save()
    return HttpResponse('success')


# debug
def reset_likes(request):
    for post in Post.objects.all():
        post.post_likes = 0
        post.save()
    return redirect('/')
