from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse
from . import api
import time
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt

from .settings import redirectHelper

##################################### Scheduler HTML
@csrf_exempt
def sched(request):
    return render(request, 'user/scheduler.html')

##################################### Base HTML
@csrf_exempt
def index(request):
    if request.session.has_key('type'):

        sendInfo = {
            'name' : request.session['name'],
            'email' : request.session['email'],
            'refresh_token' : request.session['refresh_token'],
            'picture' : request.session['picture'],
            'login_type' : request.session['type']
        }

        api.UpdateUser(sendInfo)

        return render(request, 'user/index.html', {'user':sendInfo['name']})
    else:
        return redirect(redirectHelper())

##################################### Templates
# Index Template (Today's Task)
@csrf_exempt
def mainView(request):
    if request.session.has_key('type'):
        return render(request, 'user/index-template.html')
    else:
        return redirect(redirectHelper())

# Header Template
def header(request):
    if request.session.has_key('type'):
        return render(request, 'user/header-template.html')
    else:
        return redirect(redirectHelper())

# Footer Template
def footer(request):
    if request.session.has_key('type'):
        return render(request, 'user/footer-template.html')
    else:
        return redirect(redirectHelper())

# Side-Nav Template
def sideNav(request):
    if request.session.has_key('type'):
        return render(request, 'user/side-nav-template.html')
    else:
        return redirect(redirectHelper())

# Preferences Template
def preferences(request):
    if request.session.has_key('type'):
        return render(request, 'user/preferences-template.html')
    else:
        return redirect(redirectHelper())

# Keywords Template
def keywords(request):
    if request.session.has_key('type'):
        return render(request, 'user/keywords-template.html')
    else:
        return redirect(redirectHelper())

# Missed Reminders Template
def missed(request):
    if request.session.has_key('type'):
        return render(request, 'user/missed-template.html')
    else:
        return redirect(redirectHelper())

# Reminders Template
def reminder(request):
    if request.session.has_key('type'):
        return render(request, 'user/reminders-template.html')
    else:
        return redirect(redirectHelper())

# Not Found Template
def notfound(request):
    if request.session.has_key('type'):
        return render(request, 'user/page-not-found.html')
    else:
        return redirect(redirectHelper())

# To be Done in Future
# def inbox(request):
#     if request.session.has_key('type'):
#         return render(request, 'user/inbox-template.html')
#     else:
#         return redirect(redirectHelper())

# def sent(request):
#     if request.session.has_key('type'):
#         return render(request, 'user/sent-template.html')
#     else:
#         return redirect(redirectHelper())

# def compose(request):
#     if request.session.has_key('type'):
#         return render(request, 'user/compose-template.html')
#     else:
#         return redirect(redirectHelper())