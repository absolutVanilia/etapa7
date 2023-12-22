import factory
from user.models import CustomUser
from blogs.models import Post

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post