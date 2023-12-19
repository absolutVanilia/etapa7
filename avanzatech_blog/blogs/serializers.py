from rest_framework import serializers
from .models import Post


class BlogSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='blogs_post.owner_id')

    class Meta:
        model = Post
        exclude = ('status',)
