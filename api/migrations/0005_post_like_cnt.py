# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-05 19:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_post_is_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_cnt',
            field=models.IntegerField(default=3),
        ),
    ]
