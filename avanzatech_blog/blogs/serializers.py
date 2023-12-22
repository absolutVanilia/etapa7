from rest_framework import serializers
from .models import Post, Like


class BlogSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='blogs_post.owner_id')

    class Meta:
        model = Post
        exclude = ('status',)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'