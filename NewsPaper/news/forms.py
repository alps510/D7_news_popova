from django import forms
from django.contrib.auth.models import User

from .models import Post, Author


class PostForm(forms.ModelForm):

    content = forms.CharField(min_length=20)
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'content',
        ]