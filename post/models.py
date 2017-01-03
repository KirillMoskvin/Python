# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_text
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    class Meta():
        db_table = "post"

    post_text = models.TextField(verbose_name="Текст поста")
    post_date = models.DateTimeField()
    post_likes = models.IntegerField(default=0)
    post_author = models.ForeignKey(User, default=1)
    def __unicode__(self):
    	return self.post_text
    def __str__(self):
    	return self.post_text



class Comments(models.Model):
    class Meta():
        db_table = 'сomments'

    comments_text = models.TextField()
    comments_article = models.ForeignKey(Post)


class Profile(models.Model):
    class Meta:
        db_table = 'user_profile'

    profile_user = models.OneToOneField(User)
    profile_likes = models.ManyToManyField(Post)
    profile_subscribes = models.ForeignKey('self')
