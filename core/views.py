from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse

from .settings import redirectHelper

##################################### Base HTML
def index(request):
    if request.session.has_key('type'):
        return redirect(redirectHelper() + "user")
    else:
        return render(request, 'core/index.html')

#####################################

##################################### Templates
# Index Template
def mainView(request):
    return render(request, 'core/index-template.html')

# Header Template
def header(request):
    return render(request, 'core/header-template.html')

# Footer Template
def footer(request):
    return render(request, 'core/footer-template.html')

# Plugin Template
def plugin(request):
    return render(request, 'core/plugin-template.html')

# Mobile App Template
def mobile(request):
    return render(request, 'core/mobile-template.html')

# Not Found Template
def notfound(request):
    return render(request, 'core/page-not-found.html')

#####################################