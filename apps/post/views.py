from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from apps.post.forms import PostForm
from apps.post.models import Post


class AddPost(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'post/add_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data
            category_obj = Post(**validated_data)
            category_obj.save()
            return redirect('ok')
        return render(request, 'post/add_post.html', {'form': form})


class PostList(ListView):
    model = Post
