from django.db import models

# Create your models here.

class Post(models.Model):
    """
    A class representing a blog post.
    """

    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('authenticated', 'Authenticated'),
        ('team', 'Team'),
        ('owner', 'Owner'),
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    reading_permission = models.CharField(max_length=15, choices=VISIBILITY_CHOICES, default='public')
    writing_permission = models.CharField(max_length=15, choices=VISIBILITY_CHOICES, default='owner')
    status = models.BooleanField(default=1)

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

class Like(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')