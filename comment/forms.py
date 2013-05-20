from django import forms
from comment.models import Comment
from django.template import Template, Context, loader
from django.utils.translation import gettext as _
from django.core.urlresolvers import reverse


class BaseCommentForm(forms.ModelForm):
    next_page = forms.CharField(widget=forms.HiddenInput())
    root_ctype_name = forms.CharField(widget=forms.HiddenInput())
    root_object_id = forms.CharField(widget=forms.HiddenInput())
    parent_comment = forms.CharField(widget=forms.HiddenInput(), initial=0)
    comment_type = forms.CharField(widget=forms.HiddenInput)

    def __unicode__(self):
        template = loader.get_template('comment/form.html')
        return template.render(Context({'form': self}))


class AnonymousCommentForm(BaseCommentForm):
    COMMENT_TYPE = 'ANONYMOUS'
    DEFAULT_STATUS = 'PENDING'
    commented_by_fullname = forms.CharField(max_length=100, required=True,
                                            label=_('Full name'))
    commented_by_email = forms.EmailField(required=True, label=_('E-mail'))
    comment_type = forms.CharField(widget=forms.HiddenInput(),
                                   initial=COMMENT_TYPE)
    status = forms.CharField(widget=forms.HiddenInput(),
                             initial=DEFAULT_STATUS)

    def get_error_message(self):
        return _('Your comment could not be saved')

    def get_success_message(self):
        return _('Your comment was saved succesfully. And we send an email '
                 'to confirm your email. Your comment will be showed after'
                 ' e-mail confirmation')

    class Meta:
        model = Comment
        fields = ('commented_by_fullname', 'commented_by_email', 'comment',
                  'root_object_id', 'parent_comment', 'status')


class AuthorizedCommentForm(BaseCommentForm):
    COMMENT_TYPE = 'AUTHORIZED'
    DEFAULT_STATUS = 'APPROVED'
    comment_type = forms.CharField(widget=forms.HiddenInput(),
                                   initial=COMMENT_TYPE)
    status = forms.CharField(widget=forms.HiddenInput(),
                             initial=DEFAULT_STATUS)
    def get_error_message(self):
        return _('Your comment could not be saved')

    def get_success_message(self):
        return _('Your comment was saved succesfully')

    class Meta:
        model = Comment
        fields = ('root_object_id', 'parent_comment', 'comment', 'status')
