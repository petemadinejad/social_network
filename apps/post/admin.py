from django.contrib import admin

from apps.post.models import Like, Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['body', 'user']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'body']
