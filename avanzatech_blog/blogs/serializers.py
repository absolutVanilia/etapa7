from rest_framework import serializers
from .models import Post

class BlogSerializer(serializers.Model):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['id', 'created', 'modified', 'owner', 'title', 'content', 'status']
