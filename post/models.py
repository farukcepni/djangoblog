from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from comment.models import Comment
from django.core.cache import get_cache


class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255, verbose_name=_('title'))
    slug = models.SlugField(max_length=255, verbose_name=_('slug'))
    content = models.TextField(verbose_name=_('post'))
    status = models.CharField(max_length=10,
                              choices=(
                                  ('DRAFT', 'Draft'),
                                  ('PUBLISHED', 'Published'),
                                  ('DECLINED', 'Declined')
                              ),
                              default='DRAFT', verbose_name=_('status'))
    added_time = models.DateTimeField(auto_now_add=True, auto_now=False,
                                      verbose_name=_('added time'))
    last_modified_time = models.DateTimeField(auto_now=True)
    comments = generic.GenericRelation(Comment)


    @property
    def summary(self):
        return self.content[0:300]

    def posted_by(self):
        if self.user.first_name == '' or self.user.last_name == '':
            return self.user.email
        return self.user.first_name + ' ' + self.user.last_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save()

    @classmethod
    def get(cls, post_id):
        cache_key = 'POST_'+str(post_id)
        cache = get_cache('default')
        post = cache.get(cache_key)
        if not post:
            try:
                post = Post.objects.select_related().get(id=post_id)
            except:
                post = None
            cache.set(cache_key, post, 60*10)
        return post

    class Meta:
        db_table = 'post'
        ordering = ['-added_time']
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __unicode__(self):
        return self.title



# Create your models here.
