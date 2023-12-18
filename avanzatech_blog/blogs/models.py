from django.conf import settings
from django.db import models

# Create your models here.

class Post(models.Model):
    """
    A class representing a blog post.
    """

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('authenticated', 'Authenticated'),
        ('team', 'Team'),
        ('owner', 'Owner'),
    ]

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs', null=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    visibility = models.CharField(max_length=15, choices=VISIBILITY_CHOICES, default='public')
    status = models.BooleanField(default=True)
    