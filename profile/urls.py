from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^signup/$', 'profile.views.signup', name='signup'),
    url(r'^signup_success/$', 'profile.views.signup_success',
        name='signup_success'),
    url(r'^login', 'profile.views.login_view', name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
    url(r'^edit', 'profile.views.edit', name='profile_edit'),
    url(r'^password_change$', 'django.contrib.auth.views.password_change',
        {'template_name': 'profile/password_change.html'},
        name='password_change'),
    url(r'^password_change_done$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'profile/password_change_done.html'},
        name='password_change_done'),
    url(r'^activate_the_profile$', 'profile.views.activate_the_profile',
        name='activate_the_profile'),
    url(r'([\a-zA-Z0-9-]+)', 'profile.views.profile', name='profile'),
    url(r'^$', 'profile.views.index', name='profile_index')
)