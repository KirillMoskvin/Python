# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20161220_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_text',
            field=models.TextField(verbose_name='Текст поста'),
        ),
    ]
