from django.contrib.admindocs.tests import fields
from django import forms
from post.models import Post


class PostForm(forms.ModelForm):
    status = forms.ChoiceField(widget=forms.Select(),
                               choices=(Post._meta.get_field('status')
                                            .choices[0:2]))

    class Meta:
        model = Post
        fields = ('title', 'content', 'status')

