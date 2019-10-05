# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-05 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_post_ceil'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='ceil',
            new_name='ceil_done',
        ),
        migrations.AddField(
            model_name='post',
            name='ceil_progress',
            field=models.IntegerField(default=20),
        ),
    ]