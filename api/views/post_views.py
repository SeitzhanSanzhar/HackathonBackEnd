from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.serializers import *
from api.models import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.middleware import get_user

class ListCreatePostInProcess(generics.ListCreateAPIView):
    serializer_class = PostInProcess
    def get_queryset(self):
        res = sorted(PostInProcess.objects.all(), key=lambda t: -t.repost_amount)
        return res

class ListCreatePosts(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        res = sorted(Post.objects.all(), key=lambda t: -t.like_amount)
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
    post = Post.objects.get(id=pk)

    mr = Repost(reposter = user, post = post)
    mr.save()

    return Response(post.repost(user))

@api_view(['GET'])
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