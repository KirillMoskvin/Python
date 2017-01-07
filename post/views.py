from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, render
from django.template import Context
from django.template.loader import get_template
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from django.template import RequestContext

from post.forms import PostForm
from post.models import Post, Profile

import datetime


# Create your views here.

# декоратор для проверки на авторизацию
def auth_required(function):
    def check_auth(request, *args, **kwargs):
        if not request.user.is_authenticated(): #если пользователь не авторизован, отправляем его регистрироваться
            return HttpResponseRedirect('/auth/login/')
        return function(request, *args, **kwargs)

    return check_auth


# старый индекс, не используется
def posts(request):
    args = {'posts': Post.objects.all().order_by('-post_date'),  # посты, отсортированные по убыванию даты
            'post_form': PostForm,  # форма для поста
            'user': auth.get_user(request),  # авторизованный юзер
            'target_user': auth.get_user(request)}
    args.update(csrf(request))
    return render_to_response('posts.html', args)


def posts_of_user(request, user_id):
    return render_to_response('posts.html', {'posts': Post.objects.filter(post_id=user_id)})


# добавление лайка
def addlike(request, post_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/auth/login/')
    try:
        if request.POST:
            post = Post.objects.get(id=post_id) # ищем нужный пост
            profile = Profile.objects.get(profile_user=auth.get_user(request))  # ищем профиль юзера
            if post in profile.profile_likes.all():  # если лайк уже есть, снимаем его
                post.post_likes -= 1
                profile.profile_likes.remove(post)
                profile.save()
                post.save()
            else:  # иначе ставим
                post.post_likes += 1
                profile.profile_likes.add(post)
                post.save()
                profile.save()
    except ObjectDoesNotExist:
        raise Http404
    c = {}
    c.update(csrf(request))
    return redirect(request.META['HTTP_REFERER'])
    #return redirect('/user/' + str(Post.objects.get(id=post_id).post_author_id) + '/', RequestContext(request, {}))


@auth_required
def addpost(request):
    if request.POST:
        form = PostForm(request.POST)  # вытаскиваем форму из запроса
        if form.is_valid():  # если данные валидны, сохраняем пост
            post = form.save(commit=False)
            post.post_date = datetime.datetime.now()
            post.post_author_id = request.user.id
            form.save()
    return redirect('/posts')


#  список всех юзеров
def indexusers(request):
    args = {'users': User.objects.all(), 'user': auth.get_user(request)}
    return render_to_response('indexusers.html', args)


# индекс
def getuserwall(request, user_id):
    try:
        args = {'target_user': User.objects.get(id=user_id),  # на чьей странице
                'posts': Post.objects.all().order_by('-post_date'),  # посты, отсортированные по дате
                'user': auth.get_user(request)  # кто зарегистрирован
                }
        if args['target_user'].id == args['user'].id:  # если на своей странице,
            args['post_form'] = PostForm()    # добавляем форму для поста
        # если подписаны на текущего бзера
        if Profile.objects.get(profile_user=args['target_user']) in Profile.objects.get(profile_user=args['user']).profile_subscribes.all():
            args['subscribed'] = True
        else:
            args['subscribed'] = False
        # безопасность типа
        args.update(csrf(request))
        return render_to_response('posts.html', args)
    except ObjectDoesNotExist:
        raise Http404


# добавление подписки
@auth_required
def add_subscribe(request, user_id):
    try:
        user = auth.get_user(request)
        current_profile = Profile.objects.get(profile_user=user)  # профиль тек. юзера
        if user_id != user.id:
            user_to_sub = Profile.objects.get(profile_user=User.objects.get(id=user_id))  # на кого подписываемся
            if user_to_sub in current_profile.profile_subscribes.all():  # если уже подписаны, то отписываемся
                current_profile.profile_subscribes.remove(user_to_sub)
            else:
                current_profile.profile_subscribes.add(user_to_sub)
            current_profile.save()
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/user/'+str(user_id)+'/')


# новостная лента пользователя
@auth_required
def feed(request):
    profile = Profile.objects.get(profile_user=auth.get_user(request))  # чей фид
    # ищем посты тех, на кого подписаны
    all_subscribes = profile.profile_subscribes.all()
    subscribes = []
    for sub in all_subscribes:
        subscribes.append(sub.profile_user)

    args = {'user_feed': Post.objects.filter(post_author__in=subscribes).order_by('-post_date'),
            'user': auth.get_user(request)}
    return render_to_response('feed.html', args)


# debug, создание профилей
def init_profiles(request):
    for user in User.objects.all():
        user_profile = Profile(profile_user=user)
        user_profile.save()
    return HttpResponse('success')


# debug, обнуление всех лайков
def reset_likes(request):
    for post in Post.objects.all():
        post.post_likes = 0
        post.save()
    return redirect('/')
