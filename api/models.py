from __future__ import unicode_literals
from django.contrib.auth.models import User,AnonymousUser
from rest_framework import status
from django.db import models

class Post(models.Model):

    STATUSES = NEW, IN_PROGRESS, DONE = range(3)

    author = models.CharField(max_length=500)
    post_status = models.IntegerField(choices=zip(STATUSES,STATUSES), default=NEW)

    text = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    image = models.ImageField()

    date = models.DateTimeField()
    is_liked = models.BooleanField(default=False)
    ceil = models.IntegerField(default=200)
    like_cnt = models.IntegerField(default=3)

    def like(self, user):

        try:
            may_be_like = Like.objects.get(liker = user, post = self)
            return "already_was_liked_by_this_user"
        except:
            pass

        new_like = Like(liker = user, post = self)
        new_like.save()

        if (self.like_amount >= self.ceil):
            self.post_status = self.IN_PROGRESS
            post_in_process = PostInProcess(post=self, status = PostInProcess.WAITING_FOR_FILL)
            post_in_process.save()

        self.save()
        return status.HTTP_200_OK

    def unlike(self, user):
        try:
            may_be_like = Like.objects.get(liker = user, post = self)
            may_be_like.delete()
            return status.HTTP_200_OK
        except:
            return "already_not_liked_by_this_user"


    @property
    def like_amount(self):
        all_likes = Like.objects.filter(post = self)
        return all_likes.count()

    @property
    def percentage(self):
        return (self.like_amount * 1.0 / self.ceil * 1.0)

    def __str__(self):
        return self.title


class PostInProcess(models.Model):
    STATUSES = WAITING_FOR_FILL, LAUNCHED = range(2)
    status = models.IntegerField(choices=zip(STATUSES,STATUSES))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    company_name = models.CharField(max_length=500, default="not_filled")
    requirements = models.CharField(max_length=10000, default="not_filled")
    ceil = models.IntegerField(default=100)

    def repost(self, user):
        try:
            mr = Repost.objects.get(reposter = user, post = self)
            return "already_was_reposted_by_this_user"
        except Repost.DoesNotExist:
            pass

        nr = Repost(reposter = user, post = self)
        nr.save()
        if (self.repost_amount >= self.ceil_done):
            self.post_status = self.DONE
        self.save()
        return status.HTTP_200_OK

    @property
    def percentage(self):
        return (self.repost_amount * 1.0 / self.ceil * 1.0)

    @property
    def repost_amount(self):
        all_repost = Repost.objects.filter(post=self)
        return all_repost.count()

    def __str__(self):
        return self.post.title


class Report(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    text = models.CharField(max_length=500)
    image = models.ImageField()
    youtube_link = models.CharField(max_length=500)


class Like(models.Model):

    liker = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.post.title

class Repost(models.Model):
    reposter = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.post.title
