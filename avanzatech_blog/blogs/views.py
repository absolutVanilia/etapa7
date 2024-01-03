from .serializers import BlogSerializer, LikeSerializer, CommentSerializer
from .models import Post, Like, Comment
from rest_framework import generics, mixins, response, status
from rest_framework.permissions import IsAuthenticated
from utils.custom_permissions import IsOwnerOrIsAdminPermission
from utils.pagination import PostsResultsSetPagination, LikesResultsSetPagination
from django.shortcuts import get_object_or_404
from utils.queryset import ReadQuerySet, UpdateQuerySet, LikeQuerySet, CommentQuerySet
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

class RetrieveSpecificBlogPost(ReadQuerySet, generics.RetrieveAPIView):
    '''
    This class is associated with the /post/<int:pk> endpoint, 
    it retrives a specific blog post based on the provided ID.
    The queryset method is inherit from ReadQuerySet.
    '''
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    
class UpdateBlogPost(UpdateQuerySet, generics.UpdateAPIView):
    '''
    This class is associated with the /blog/<int:pk> endpoint,
    it allows Post owner, users with updates permision, and admins to update a post
    The queryset method is inherit from UpdateQuerySet.

    '''
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrIsAdminPermission]

class DeleteBlogPost(UpdateQuerySet,generics.DestroyAPIView):
    '''
    This class is associated with the /delete/<int:pk> endpoint,
    it allows Post owner and admins to delete a post
    The queryset method is inherit from UpdateQuerySet.
    '''
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrIsAdminPermission]

class LikeUnlike(ReadQuerySet, generics.GenericAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]
    
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
    
class LikeList(LikeQuerySet, generics.ListAPIView):
    serializer_class = LikeSerializer
    pagination_class = LikesResultsSetPagination
    permission_classes = [IsAuthenticated]

class CreateCommentDeleteComment(LikeUnlike, ReadQuerySet, generics.GenericAPIView, mixins.CreateModelMixin, mixins.DestroyModelMixin,):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def post(self, request, pk):
        post = self.get_post_object(pk)
        comment = Comment.objects.create(owner=request.user, post=post, content=request.data['content'])
        return response.Response(self.get_serializer(comment).data, status=status.HTTP_201_CREATED)
        
    def delete(self, request, pk):
        post = self.get_post_object(pk)
        comment = Comment.objects.filter(owner=request.user, post=post).first()
        comment.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(CommentQuerySet, generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = PostsResultsSetPagination
    permission_classes = [IsOwnerOrIsAdminPermission]


    
