from rest_framework import serializers
from .models import Post, Comment, Like


class BlogSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='blogs_post.owner_id')

    class Meta:
        model = Post
        exclude = ('status',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

