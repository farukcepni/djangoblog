from django.http import  Http404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from post.models import Post
from post.forms import PostForm
from image.models import Image
from django.db import connection, connections
from django.views.decorators.cache import cache_page
from django.core.cache import get_cache


def post_view(request, post_slug, post_id):
    post = Post.get(post_id)
    if not post:
        raise Http404('The post could not be found')

    if post.status != 'PUBLISHED' and post.user_id != request.user.id \
            or post.slug != post_slug:
        raise Http404('The post could not be found.')
    comments = post.comments.all()
    return render(request, 'post/view.html', {'post': post,
                                              'comments': comments})


def post_list(request, username=None):
    post_list = Post.objects.order_by('-added_time').select_related()
    post_list = post_list.filter(status='PUBLISHED') | \
        post_list.filter(status='DRAFT', user_id=request.user.id)
    if username is not None:
        user = get_object_or_404(User, username=username)
        post_list = post_list.filter(user_id=user.id)
    return render(request, 'post/list.html', {'post_list': post_list})


@login_required
def save_post(request, post_id=None):
    post = post_id is None and Post(user_id=request.user.id) \
        or get_object_or_404(Post, id=post_id)
    if request.POST:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('edit_post', post.id)
    else:
        form = PostForm(instance=post)
    images = Image.objects.filter(user_id=request.user.id)
    form.new = post_id is None or False
    return render(request, 'post/form.html', {'form': form,
                                              'images': images})
