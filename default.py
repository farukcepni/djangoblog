from django.shortcuts import render


def page_not_found(request):
    return render(request, '404.html', {'message': 'Page Not Found'})

def server_error(request):
    return render(request, '500.html', {'message': 'Server Error'})