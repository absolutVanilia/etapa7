from blogs.models import Post
from django.db.models import Q

class ReadQuerySet:
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            return Post.objects.all()
    
        if user.is_authenticated:
            return Post.objects.filter(
                Q(read_permission='public') | 
                Q(read_permission='authenticated') | 
                Q(owner=user) | 
                Q(owner__team=user.team) & 
                Q(is_active=True))
        
        return Post.objects.filter(Q(read_permission='public'))