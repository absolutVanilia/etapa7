import factory
from user.models import CustomUser
from blogs.models import Post, Comment, Like

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email     = factory.Sequence(lambda n: f'user{n}@gmail.com')
    team      = factory.Sequence(lambda n: n)
    is_staff  = True
    is_active = True

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    owner = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f'post{n}')
    content = factory.Sequence(lambda n: f'post{n} content')
    reading_permission = factory.Sequence(lambda _: 'public')
    writing_permission = factory.Sequence(lambda _: 'public')

class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Like

    owner = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    content = factory.Sequence(lambda n: '')
    owner = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)