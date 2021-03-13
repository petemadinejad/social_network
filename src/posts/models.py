from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile


# Create your models here.


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
                              blank=True)
    #  validators that are allowed  are passed to FileExtensionValidator
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    # related name works when there is  reverse relationship
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        """return number of likes for a post"""
        return self.liked.all().count()

    # num of comments here
    def num_comments(self):
        return self.comment_set.all().count()

    class Meta:
        """newest post will be at the top and the oldest at the bottom"""
        ordering = ('-created',)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


LIKE_CHOICE = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    """purpose of the class is have a track of the likes,we will know when a particular user gave a like and to what post
    the user gave the like and when a particular user decided to unlike we will store it in updated field and the first
    like is store in created field"""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICE, max_length=8)
    # value will be either like or unlike
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.user, self.post, self.value)

