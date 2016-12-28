from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect,render
from django.template import Context
from django.template.loader import get_template
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from post.models import Post
from post.forms import PostForm



