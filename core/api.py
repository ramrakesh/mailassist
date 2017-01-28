from apiclient import discovery
import httplib2
from oauth2client import client
import logging

from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse
import time
import requests
import json

from .settings import redirectHelper

##################################### Oauth Objects
# Google API Auth Object
flow = client.OAuth2WebServerFlow(
    client_id = '529425540533-b3gvjh0sor2rol0oetdhvkvdp4radmrh.apps.googleusercontent.com',
    client_secret = 'iDFfL3Vfrxg81ZAxa8aDesVb',
    scope = 'https://mail.google.com/ https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/gmail.send')

#####################################

##################################### Logins
# Gmail Login
def gmailLogin(request): # Google Login Step 1
    
    if request.session.has_key('type'):
        return redirect(redirectHelper()+"user")
    else:
        global flow
        callback = redirectHelper()+'gmailCallback/oauth2callback'
        authorize_url = flow.step1_get_authorize_url(callback)
        return redirect(authorize_url)

# Gmail Login CallBack
def gmailLoginStep2(request): # Google Login Step 2

    global flow
    auth_code = request.GET['code'];
    credentials = flow.step2_exchange(auth_code)
    
    # Session
    request.session['type'] = 'gmail'
    request.session['access_token'] = credentials.access_token
    request.session['refresh_token'] = credentials.refresh_token
    request.session['session_start_time'] = time.time()
    request.session['email'] = credentials.id_token['email']
    request.session['name'] = credentials.id_token['name']
    if(credentials.id_token.has_key('picture')):
        request.session['picture'] = credentials.id_token['picture']
    else:
        request.session['picture'] = ''

    return redirect(redirectHelper()+"user")

#####################################

##################################### Logout
# Logout
def logout(request): # Google Logout
    try:
        del request.session['type']
    except:
        pass
    return redirect(redirectHelper())
    
#####################################

##################################### Plugin
# Check Session
def checkPluginSession(request):
    if request.session.has_key('type'):
        return HttpResponse(json.dumps({'session':True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'session':False}), content_type="application/json")

# Check Message Text
def checkMessageText(request):
    if request.session.has_key('type'):
        user = getUser(email = request.session['email'])
        keywords = keywordsGetPlugin(user)
        message = request.POST['message'];
        respObj = getRems(message,keywords)
        resp = {'done':True,'rems': respObj}
        return HttpResponse(json.dumps({'session':True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

#####################################