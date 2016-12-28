# -*- coding: utf-8 -*-
__author__ = 'mj'

from django.forms import ModelForm
from django import forms
from post.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post  # привязка к модели
        fields = ['post_text']
