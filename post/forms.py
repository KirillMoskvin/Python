# -*- coding: utf-8 -*-
__author__ = 'mj'

from django.forms import ModelForm
from models import Post

class PostForm(ModelForm)
	class Meta:
		model = Post #привязка к модели
	