# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-06 00:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_postinprocess_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='postinprocess',
            name='percentage_val',
            field=models.IntegerField(default=0),
        ),
    ]
