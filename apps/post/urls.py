from django.urls import path

from apps.post.views import AddPost, PostList

urlpatterns = [

    path('addpost/', AddPost.as_view(), name='addpost'),
    path('listpost/', PostList.as_view(), name='listpost'),
]
