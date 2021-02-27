from datetime import datetime

from django.db import models
from django_extensions.db.fields import AutoSlugField
from apps.account.models.user import User
from apps.profile_user.models import Profile


class Post(models.Model):
    body = models.TextField(verbose_name='Body')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='created_at', default=datetime.now())

    def __str__(self):
        return "{}".format(self.body)[:30]

    class Meta:
        ordering = ('-created_at',)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(verbose_name='Text Of Comment')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True)

    def __str__(self):
        return "{} add a comment for post {}".format(self.user, self.post)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now=True)

    def __str__(self):
        return "{} like post {}".format(self.user, self.post)
