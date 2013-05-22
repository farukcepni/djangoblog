from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from post.models import Post
from post.forms import PostForm
from image.models import Image
from comment.forms import AuthorizedCommentForm, AnonymousCommentForm
from comment.models import Comment
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType


def post_view(request, post_slug, post_id):
    post = Post.get(post_id)
    if not post:
        raise Http404('The post could not be found')

    if post.status != 'PUBLISHED' and post.user_id != request.user.id \
            or post.slug != post_slug:
        raise Http404('The post could not be found.')

    comments = Comment.get_comments(post)
    if post.status != 'DRAFT':
        comment_form = request.user.is_authenticated() and\
            AuthorizedCommentForm or AnonymousCommentForm
        comment_form = comment_form(initial={
            'root_ctype_id': ContentType.objects.get_for_model(Post).id,
            'root_object_id': post.id,
            'next_page': reverse('post', args=[post.slug, post.id])})
    else:
        comment_form = None
    return render(request, 'post/view.html', {'post': post,
                                              'comments': comments,
                                              'comment_form': comment_form})


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
