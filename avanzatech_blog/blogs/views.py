from django.shortcuts import render
from .serializers import BlogSerializer, LikeSerializer
from .models import Post, Like
from rest_framework import generics, mixins, response, status
from rest_framework.permissions import IsAuthenticated
from .custom_permissions import IsOwnerOrIsAdminPermission
from utils.pagination import PostsResultsSetPagination, LikesResultsSetPagination
from django.shortcuts import get_object_or_404
from utils.queryset import ReadQuerySet
from django.db.models import Q

# Create your views here.

class CreateBlogPost(generics.ListCreateAPIView):
    '''
    This class is associated with the /post endpoint, 
    it allows authenticated users to create a post
    '''
    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostsResultsSetPagination


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

class CreateLikeDeleteLike(ReadQuerySet, generics.GenericAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwnerOrIsAdminPermission]
    
    def get_post_object(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)
    
    def post(self, request, pk):
        post = self.get_post_object(pk)
        like, created = Like.objects.get_or_create(owner=request.user, post=post)
        if not created:
            return response.Response({'detail': 'You already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(self.get_serializer(like).data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        post = self.get_post_object(pk)
        like = get_object_or_404(Like, owner=request.user, post=post)
        like.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
    
class LikeList(ReadQuerySet, generics.ListAPIView):
    serializer_class = LikeSerializer
    pagination_class = LikesResultsSetPagination
    

    def get_queryset(self):
        if self.request.user.role == 'admin':
            queryset = Like.objects.all()
        else:        
            queryset = Like.objects.filter(Q(post__read_permission='public') | Q(post__read_permission='authenticated')
                                       | Q(post__author=self.request.user) | Q(post__author__team=self.request.user.team) & Q(post__is_active=True))
        
        post = self.request.query_params.get('post', None)
        user = self.request.query_params.get('user', None)
        if post is not None:
            queryset = queryset.filter(post=post)
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset
    
