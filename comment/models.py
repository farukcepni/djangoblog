from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.utils.datastructures import SortedDict
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Comment(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    comment = models.CharField(max_length=255, verbose_name=_('comment'))
    status = models.CharField(max_length=10,
                              choices=(('PENDING', 'Pending'),
                                       ('APPROVED', 'Approved'),
                                       ('DECLINED', 'Declined')),
                              verbose_name=_('status'))
    added_time = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('added time'))

    class Meta:
        db_table = 'comment'
        ordering = ['added_time']

    def get_children(self):
        content_type = ContentType.objects.get(app_label='comment',
                                               model='comment')
        comments = Comment.objects.filter(content_type=content_type,
                                          object_id=self.id)
        return comments

    @classmethod
    def convert_tree(cls, post_id):
        comments = cls.objects.filter(post_id=post_id).order_by('added_time')
        import copy
        comment_tree = SortedDict({0: {'children': SortedDict({})}})
        parent_tree = {0: (0, )}

        for comment in comments:
            comment = copy.deepcopy(comment)
            comment.children = SortedDict({})
            parent = parent_tree[comment.parent]
            if comment.parent == 0:
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
                inst_ct[comment.parent].children[comment.id] = comment
                parent_tree[comment.id] = parent + (comment.parent,)
        return comment_tree[0]['children']

