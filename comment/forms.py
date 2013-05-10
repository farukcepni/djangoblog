from django import forms
from comment.models import Comment
from post.models import Post
from django.contrib.contenttypes import generic

class AddComment(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment', )