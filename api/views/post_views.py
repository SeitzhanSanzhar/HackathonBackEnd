from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.serializers import *
from api.models import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


class ListCreatePosts(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #permission_classes = [IsAuthenticated]
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class RetrieveUpdateDestroyPosts(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

@api_view(['POST'])
def like(request):
    pk = request.data.get('post_id')
    token = Token.objects.get(key=request.auth)
    user = User.objects.get(id = token.user_id)
    posts = Post.objects.get(id = pk)
    post = posts
    may_be_like = Like.objects.filter(liker = user, post = post)
    if (may_be_like != None):
        return Response("already was liked")
    new_like = Like(liker = user, post = post)
    new_like.save()
    return new_like

@api_view(['GET'])
def get_like_amount(request):
    pk = request.data.get('post_id')
    post = Post.objects.get(id=pk)
    res = {
        "like_amount": post.like_amount
    }
    return Response(res)