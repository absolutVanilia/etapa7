from blogs.models import Post, Like, Comment
from django.db.models import Q

class ReadQuerySet:
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            return Post.objects.all()
    
        if user.is_authenticated:
            return Post.objects.filter(
                Q(reading_permission='public') |
                Q(reading_permission='authenticated') |
                Q(owner=user) | 
                Q(owner__team=user.team))
        
        return Post.objects.filter(read_permission='public')

class UpdateQuerySet:
    def get_queryset(self, *args, **kwargs):
        user = self.request.user

        if user.is_authenticated:
            if user.is_staff:
                return Post.objects.all()
            
            return Post.objects.filter(Q(edit_permission='public') | 
                                       Q(edit_permission='authenticated') | 
                                       Q(author=user) | 
                                       Q(author__team=user.team))
        
        print("user not authenticated")
        return Post.objects.filter(edit_permission='public')

class LikeQuerySet:
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                queryset = Like.objects.all()
            else:        
                queryset = Like.objects.filter( 
                    Q(post__read_permission='public') | 
                    Q(post__read_permission='authenticated') | 
                    Q(post__author=user, post__read_permission='author') | 
                    Q(post__author__team=user.team, post__read_permission='team'))
        else:
            queryset = Like.objects.filter(post__read_permission='public')
                   
        post = self.request.query_params.get('post', None)
        user = self.request.query_params.get('user', None)
        if post is not None:
            queryset = queryset.filter(post=post)
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset

class CommentQuerySet:
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            queryset = Comment.objects.all()
        else:        
            queryset = Comment.objects.filter(
                Q(post__read_permission='public') | 
                Q(post__read_permission='authenticated') | 
                Q(post__author=user) | 
                Q(post__author__team=user.team))
        
        post = self.request.query_params.get('post', None)
        user = self.request.query_params.get('user', None)
        if post is not None:
            queryset = queryset.filter(post=post)
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset