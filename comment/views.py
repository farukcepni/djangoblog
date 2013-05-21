from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType
from comment.forms import AnonymousCommentForm, AuthorizedCommentForm
from django.contrib import messages
from comment.models import Comment
from django.core.signing import Signer
from django.shortcuts import Http404, HttpResponse
from django.utils.translation import ugettext as _

def create_comment(request):
    redirect_page = 'index'
    if request.POST:
        redirect_page = request.POST.get('next_page')
        form = request.POST.get('comment_type') ==\
            AnonymousCommentForm.COMMENT_TYPE and\
            AnonymousCommentForm(request.POST) or\
            AuthorizedCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.commented_by_user = request.user.is_authenticated()\
                and request.user or None
            new_comment.root_ctype = ContentType.objects.get(
                app_label='post', model='post')
            new_comment.save(True)
            if new_comment.status == 'PENDING':
                new_comment.send_email_to_confirm()
            messages.success(request, form.get_success_message())
        else:
            messages.error(request, form.get_error_message())
            for key, value in form.errors.items():
                messages.error(request, form.fields[key].label + ':' + value[0])

    return redirect(redirect_page)


def confirm_via_email(request):
    """
    Confirm the comment via email,
    the link contain a get parameter(comment) hashed with Signer
    """
    try:
        comment_id = int(Signer().unsign(request.GET.get('comment')))
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise Http404('The page could not be found')
    if comment.status == 'APPROVED':
        return HttpResponse(_('Your comment has been already APPROVED'))
    elif comment.status == 'DECLINED':
        return HttpResponse(_('Your comment has been DECLINED'))
    # the comment is pending and convert to approved it
    comment.status = 'APPROVED'
    comment.save()
    return HttpResponse(_('Your comment has been confirmed successfully'))