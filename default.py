from django.shortcuts import render
from django.utils.translation import ugettext as _


def page_not_found(request):
    return render(request, '404.html', {'message': _('Page Not Found')})

def server_error(request):
    return render(request, '500.html', {'message': _('Server Error')})