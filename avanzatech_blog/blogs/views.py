from django.shortcuts import render
from .serializers import BlogSerializer
from .models import Post
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from .custom_permissions import IsOwnerOrIsAdminPermission
# Create your views here.

class CreateBlogPost(generics.ListCreateAPIView):
    '''
    This class is associated with the /post endpoint, 
    it allows authenticated users to create a post
    '''
    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RetrieveSpecificBlogPost(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    

class UpdateBlogPost(generics.UpdateAPIView):
    '''
    This class is associated with the /blog/<int:pk> endpoint,
    it allows Post owner and admins to update a post
    '''
    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrIsAdminPermission]


class DeleteBlogPost(generics.DestroyAPIView):
    '''
    This class is associated with the /blog/<int:pk> endpoint,
    it allows Post owner and admins to delete a post
    '''

    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrIsAdminPermission]

class LikeAndUnlike(mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrIsAdminPermission]
