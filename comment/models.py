from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.utils.datastructures import SortedDict
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse


class Comment(models.Model):
    CHOICES_FOR_USER = (('PENDING', 'Pending'), ('APPROVED', 'Approved'))
    CHOICES_FOR_ADMIN = (('DECLINED', 'Declined'), )
    CHOICES = CHOICES_FOR_USER + CHOICES_FOR_USER

    commented_by_user = models.ForeignKey(User, blank=True, null=True)
    commented_by_fullname = models.CharField(max_length=100, blank=True)
    commented_by_email = models.EmailField(blank=True)
    root_ctype = models.ForeignKey(ContentType, related_name='root',
                                   limit_choices_to={"model__in": "Post"})
    root_object_id = models.PositiveIntegerField()
    parent_comment = models.PositiveIntegerField()
    comment = models.CharField(max_length=255, verbose_name=_('comment'))
    status = models.CharField(max_length=10,
                              choices=CHOICES,
                              verbose_name=_('status'))
    added_time = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('added time'))

    class Meta:
        db_table = 'comment'
        ordering = ['added_time']

    def commented_by(self):
        if self.commented_by_user:
            return self.commented_by_user.get_full_name() or \
                self.commented_by_user.username
        else:
            return self.commented_by_fullname or self.commented_by_email

    @classmethod
    def get_comments(cls, obj):
        comments = cls.objects.select_related('commented_by_user').filter(
            root_ctype=ContentType.objects.get_for_model(obj),
            root_object_id=obj.id)
        comments = comments.filter(status='APPROVED')
        parent_tree = {0: (0, )}
        comment_tree = SortedDict({0: {'children': SortedDict({})}})
        for comment in comments:
            comment.children = SortedDict({})
            parent = parent_tree[comment.parent_comment]
            if comment.parent_comment == 0:
                comment_tree[0]['children'][comment.id] = comment
                parent_tree[comment.id] = parent
            else:
                inst_ct = comment_tree
                for own_parent in parent:
                    inst_ct = inst_ct[own_parent]
                    if own_parent == 0:
                        inst_ct = inst_ct['children']
                    else:
                        inst_ct = inst_ct.children
                inst_ct[comment.parent_comment].children[comment.id] = comment
                parent_tree[comment.id] = parent + (comment.parent_comment,)
        return comment_tree[0]['children']

    def send_email_to_confirm(self):
        from django.core.mail import send_mail
        from django.core.signing import Signer
        from django.conf import settings
        subject, from_mail = _('Confirm Comment'), 'no-reply@blog.com'
        to = [self.commented_by_email]
        activation_url = settings.BASE_URL + \
            reverse('confirm_comment') + '?comment=' + \
            Signer().sign(self.id)
        message = 'Confirm to your comment ' + self.comment + \
                  "\r\n" + activation_url
        send_mail(subject, message, from_mail, to)
