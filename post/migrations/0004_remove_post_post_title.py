# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 21:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20161228_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_title',
        ),
    ]
