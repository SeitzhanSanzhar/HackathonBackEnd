# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-05 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_statues',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2)], default=0),
        ),
    ]