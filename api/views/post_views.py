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
    def get_queryset(self):
        res = sorted(Post.objects.all(), key=lambda t: -t.like_amount)
        user = self.request.user
        for x in res:
            try:
                like = Like.objects.get(post = x, liker = user)
                x.is_liked = True
            except Like.DoesNotExist:
                x.is_liked = False
            x.save()
        return res
    # def get_context_data(self, **kwargs):
    #     context = super(ListCreatePosts, self).get_context_data(**kwargs)
    #     try:
    #         like = Like.get(post = context, )

class RetrieveUpdateDestroyPosts(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

@api_view(['POST'])
def like(request):

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