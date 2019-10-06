from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

class PostInProcessSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    post = PostSerializer()
    class Meta:
        model = PostInProcess
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'