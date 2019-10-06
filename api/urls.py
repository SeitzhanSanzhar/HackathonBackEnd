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
    url('post_in_process/', ListCreatePostInProcess.as_view()),
    url('is_liked/', is_liked),
    url('reports', ListCreateReport.as_view()),
    url('get_finished', ListFinishedPosts.as_view()),
    url('get_report', get_report),
]
