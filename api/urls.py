from django.conf.urls import url, include
from django.contrib import admin
from views import *

urlpatterns = [
    url('posts/', ListCreatePosts.as_view()),
    url('login/', login),
    url('logout/', logout),
    url('signup/', Signup.as_view()),
    url('like/', like),
    url('remove_l/', unlike),
    url('post_statistics/', get_like_amount),
    url('repost', repost),
]
