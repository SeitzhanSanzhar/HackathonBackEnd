from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.serializers import *
from api.models import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.middleware import get_user
from api.serializers import ReportSerializer

class ListFinishedPosts(generics.ListAPIView):
    serializer_class = PostInProcessSerializer
    def get_queryset(self):
        res = PostInProcess.objects.filter(status=PostInProcess.FINISHED)
        for x in res:
            x.post.like_cnt = x.post.like_amount
            x.repost_cnt = x.repost_amount
            x.author = x.post.author
            x.percentage_val = x.percentage
        res = sorted(res, key=lambda t: -t.post.like_amount)
        return res;

class ListCreatePosts(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        res = Post.objects.filter(post_status = Post.NEW)
        for x in res:
            x.like_cnt = x.like_amount
        res = sorted(res, key=lambda t: -t.like_amount)
        return res

class ListCreatePostInProcess(generics.ListCreateAPIView):
    serializer_class = PostInProcessSerializer
    def get_queryset(self):
        res = PostInProcess.objects.filter(status = PostInProcess.LAUNCHED)
        for x in res:
            x.repost_cnt = x.repost_amount
            x.author = x.post.author
            x.percentage_val = x.percentage
        res = sorted(res, key=lambda t: -t.repost_amount)
        return res

class ListCreateReport(generics.ListCreateAPIView):
    serializer_class = PostInProcessSerializer
    def get_queryset(self):
        res = sorted(Report.objects.all(), key=lambda t: -t.repost_amount)
        return res

class RetrieveUpdateDestroyPosts(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

@api_view(['POST'])
def like(request):
    print(request.META)
    pk = request.data.get('post_id')
    token = Token.objects.get(key=request.auth)

    user = User.objects.get(id = token.user_id)
    post = Post.objects.get(id = pk)

    return Response(post.like(user))

@api_view(['POST'])
def unlike(request):

    pk = request.data.get('post_id')
    token = Token.objects.get(key=request.auth)

    user = User.objects.get(id = token.user_id)
    post = Post.objects.get(id = pk)

    return Response(post.unlike(user))



@api_view(['GET'])
def get_like_amount(request):
    pk = request.data.get('post_id')
    post = Post.objects.get(id=pk)
    res = {
        "percentage": post.percentage,
        "like_amount": post.like_amount
    }
    return Response(res)

@api_view(['POST'])
def repost(request):
    pk = request.data.get('post_id')
    token = Token.objects.get(key=request.auth)

    user = User.objects.get(id=token.user_id)
    post_ic = PostInProcess.objects.get(id=pk)
    # post_ic = PostInProcess.objects.get(post = post)
    return Response(post_ic.repost(user))

@api_view(['POST'])
def is_liked(request):
    pk = request.data.get('post_id')
    token = Token.objects.get(key=request.auth)

    user = User.objects.get(id=token.user_id)
    post = Post.objects.get(id=pk)

    try:
        like_orm = Like.objects.get(post = post, liker = user)
        return Response(True)
    except Like.DoesNotExist:
        return Response(False)

@api_view(['POST'])
def get_report(request):
    pk = request.data.get('post_id')
    token = Token.objects.get(key=request.auth)
    post_in_process = PostInProcess.objects.get(id = pk)
    report = Report.objects.get(post_in_process=post_in_process)
    report_ser = ReportSerializer(report)
    return Response(report_ser.data)