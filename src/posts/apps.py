from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'
    verbose_name='Posts,Comments,Likes'
    # used for changing the name which is appeared in admin panel we want in the admin panel
    # 'Posts,Comments,Likes' to be shown instead of just Posts as the name of application

