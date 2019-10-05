from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework import status
from django.db import models

#Like model

class Post(models.Model):

    STATUSES = NEW, IN_PROGRESS, DONE = range(3)
    post_statues = models.IntegerField(choices=zip(STATUSES,STATUSES), default=NEW)
    text = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    image = models.ImageField()
    date = models.DateTimeField()

    ceil_progress = models.IntegerField(default=20)
    ceil_done = models.IntegerField(default=100)

    def like(self, user):
        try:
            may_be_like = Like.objects.get(liker = user, post = self)
            return "already_was_liked_by_this_user"
        except:
            pass
        new_like = Like(liker = user, post = self)
        new_like.save()
        if (self.like_amount >= self.ceil_progress):
            self.post_statues = self.IN_PROGRESS
        if (self.like_amount >= self.ceil_done):
            self.post_statues = self.DONE
        self.save()
        return status.HTTP_200_OK

    @property
    def like_amount(self):
        all_likes = Like.objects.filter(post = self)
        return all_likes.count()

    @property
    def percentage(self):
        return self.like_amount * 1.0 / self.ceil * 1.0

    def __str__(self):
        return self.title

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.post.title
