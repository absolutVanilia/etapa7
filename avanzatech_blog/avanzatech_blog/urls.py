"""
URL configuration for avanzatech_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blogs.views import CreateBlogPost, UpdateBlogPost, DeleteBlogPost, RetrieveSpecificBlogPost, LikeUnlike, LikeList, CreateCommentDeleteComment, CommentList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('post/', CreateBlogPost.as_view(), name='create-blog-post'),
    path('post/<int:pk>', RetrieveSpecificBlogPost.as_view()),
    path('blog/<int:pk>', UpdateBlogPost.as_view(), name='update-blog-post'),
    path('delete/<int:pk>', DeleteBlogPost.as_view()),
    path('like/<int:pk>', LikeUnlike.as_view()),
    path('likeslist/', LikeList.as_view()),
    path('comment/<int:pk>', CreateCommentDeleteComment.as_view()),
    path('comment/list/', CommentList.as_view()),
]
