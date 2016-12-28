# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_text


# Create your models here.
class Post(models.Model):
    class Meta():
        db_table = "post"

    post_title = models.CharField(max_length = 200)
    post_text = models.TextField(verbose_name="Текст поста")
    post_date = models.DateTimeField()
    post_likes = models.IntegerField(default=0)
    def _unicode_(self): 
    	return self.post_text



class Comments(models.Model):
    class Meta():
        db_table = 'сomments'

    comments_text = models.TextField()
    comments_article = models.ForeignKey(Post)

