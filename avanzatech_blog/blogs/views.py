from django.shortcuts import render
from .serializers import BlogSerializer
from .models import Post
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .perm import IsOwnerOrAdminPermission
# Create your views here.

class CreateBlogPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrAdminPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DeleteBlogPost(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
