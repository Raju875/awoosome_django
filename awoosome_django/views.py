from django.http import HttpResponse
from django.shortcuts import render


def error_403(request, exception=None):
    context = {'message': exception}
    template_name = 'errors/403.html'
    return render(request, template_name, context)


def error_404(request, exception=None):
    context = {'message': exception}
    template_name = 'errors/404.html'
    return render(request, template_name, context)

def error_500(request, exception=None):
    context = {'message': exception}
    template_name = 'errors/500.html'
    return render(request, template_name, context)


def csrf_failure(request, reason=""):
    template_name = 'errors/403_csrf.html'
    context = {'message': reason}
    return render(request, template_name, context)
