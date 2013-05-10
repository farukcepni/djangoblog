from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.conf import settings
from django.contrib import admin
import profile
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # admin Page

    url(r'^profile/', include('profile.urls')),
    # Profile pages - signup, login, logout and etc.

    url(r'^create_comment', 'comment.views.create_comment',
        name='create_comment'),

    url(r'^image/$', 'image.views.index', name='image_index'),
    url(r'^image/delete/(.*)[/]$', 'image.views.delete', name='delete_image'),

    url(r'^post/create_post', 'post.views.save_post', name='create_post'),
    url(r'^post/edit_post/([\d]+)', 'post.views.save_post', name='edit_post'),
    url(r'(.*)/posts[/]?$', 'post.views.post_list', name='user_posts'),
    # Show User's post $USERNAME/posts

    url(r'^post/(.*)-([\d]*)\.html$', 'post.views.post_view', name='post'),
    # Show the post $USERNAME/posts/$POST_SLUG.html

    url(r'^$', 'post.views.post_list', name='index'),
    # Show the main page (All Posts)

    url(r'^(.*)$', 'profile.views.profile')
)
