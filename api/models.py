# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

# Create your models here.

#Like model

class Post(models.Model):
    text = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    image = models.ImageField()
    date = models.DateTimeField()

    @property
    def like_amount(self):
        all_likes = Like.objects.filter(post = self)
        return all_likes.count()

    def __str__(self):
        return self.title

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
