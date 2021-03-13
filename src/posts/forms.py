from django import forms
from .models import Post, Comment
from profiles.models import Profile


class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))

    # content overridden because we wanted our form have just 2 row

    class Meta:
        model = Post
        fields = ('content', 'image',)


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))

    class Meta:
        model = Comment
        fields = ('body',)
