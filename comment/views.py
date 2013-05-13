from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
import copy
from comment.models import Comment
from django.contrib.contenttypes.models import ContentType


def create_comment(request):
    if request.POST:
        next = request.POST.get('next')
        content_type = ContentType.objects.get(
            app_label=request.POST.get('content_type'),
            model=request.POST.get('content_type'))
        object_id = request.POST.get('object_id')
        comment = Comment(user_id=request.user.id,
                          content_type=content_type,
                          object_id=object_id,
                          comment=request.POST.get('comment'),
                          status='APPROVED')
        comment.save()
        return redirect(next)
    else:
        return redirect('index')
