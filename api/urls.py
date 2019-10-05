from django.conf.urls import url, include
from django.contrib import admin
from views import *

urlpatterns = [
    url('posts/1/', RetrieveUpdateDestroyPosts.as_view()),
    url('posts/', ListCreatePosts.as_view()),
    url('login/', login),
    url('logout/', logout),
    url('signup/', Signup.as_view()),
    url('like/', like),
    url('get_like_amount/', get_like_amount),
]
