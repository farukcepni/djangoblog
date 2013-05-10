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



def comment_test(request):
    data_base = [{'id': 1, 'parent': 0, 'comment': 'First'},
            {'id': 2, 'parent': 0, 'comment': 'Second'},
            {'id': 3, 'parent': 1, 'comment': 'ID3'},
            {'id': 4, 'parent': 2, 'comment': 'ID4'},
            {'id': 5, 'parent': 3, 'comment': 'ID5'},
            {'id': 6, 'parent': 3, 'comment': 'ID6'},
            {'id': 7, 'parent': 2, 'comment': 'ID7'},
            {'id': 8, 'parent': 6, 'comment': 'ID8'},
            {'id': 9, 'parent': 4, 'comment': 'ID9'}
           ]
    #data = copy.deepcopy(data_base)
    data = data_base
    comment_tree = {0: {'children': {}}}
    parent_tree = {0: (0, )}

    for comment in data:
        comment = copy.deepcopy(comment)
        comment['children'] = {}
        parent = parent_tree[comment['parent']]
        if comment['parent'] == 0:
            comment_tree[0]['children'][comment['id']] = comment
            parent_tree[comment['id']] = parent
        else:
            inst_ct = comment_tree
            for own_parent in parent:
                inst_ct = inst_ct[own_parent]['children']
            inst_ct[comment['parent']]['children'][comment['id']] = comment
            parent_tree[comment['id']] = parent + (comment['parent'],)

    return HttpResponse('test');