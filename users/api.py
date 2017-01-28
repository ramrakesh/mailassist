from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from models import User, Settings, Reminder, Keywords, Notification
import json
import time
from datetime import datetime, timedelta
import string
import random
import requests
import base64
import email
import textproc
import schedulers
import re
from tasks import startDailyReminder, startUpcomingReminder, startMissedReminder, startDeadlineReminder

from .settings import redirectHelper,NOTIFICATION_MSG
from ast import literal_eval

##################################### Helpers

# get User
def getUser(email):
    return User.objects.get(email = email)

# Get Keywords by User
def keywordsGetPlugin(user):
    try:
        keys = Keywords.objects.filter(user = user).order_by('key')
        keysRes = {}
        for each in keys:
            if keysRes.has_key(str(each.key)):
                keysRes[str(each.key)].append(str(each.action))
            else:
                keysRes[str(each.key)] = [str(each.action)]
    except Keywords.DoesNotExist:
        keysRes = {}
    return keysRes

# Current Day Tasks Helper
def tasksGet(email):
    # Fetch Tasks for the Current Day
    user = getUser(email = email)
    today = time.strftime("%Y-%m-%d")
    tasks = Reminder.objects.filter(date = today, user = user)
    tasksRes = []
    for each in tasks:
        tasksRes.append({
            'id': each.id, 
            'task': str(each.task), 
            'sender': str(each.sender), 
            'subject': str(each.subject), 
            'content': str(each.content.encode('utf-8')), 
            'threadID': str(each.threadID), 
            'typeTask': str(each.typeTask), 
            'mailer': str(each.mailer), 
            'status': str(each.status),
            'notif': NOTIFICATION_MSG
        })
    
    return tasksRes

# All Reminders Helper
def remindersGet(email):
    # Fetch Tasks for all Days in Future
    user = getUser(email = email)
    today = time.strftime("%Y-%m-%d")
    tasks = Reminder.objects.filter(date__gte = today, user = user).order_by('date')
    tasksRes = []
    for each in tasks:
        tasksRes.append({
            'id':each.id, 
            'task':str(each.task), 
            'sender': str(each.sender), 
            'subject': str(each.subject), 
            'content': str(each.content.encode('utf-8')), 
            'threadID': str(each.threadID), 
            'typeTask': str(each.typeTask), 
            'mailer': str(each.mailer),
            'status':str(each.status), 
            'date': str(each.date),
            'notif': NOTIFICATION_MSG
        })
    return tasksRes

# All Missed Reminders Helper
def missedGet(email):
    # Fetch Tasks for all Days in Future
    user = getUser(email = email)
    today = time.strftime("%Y-%m-%d")
    tasks = Reminder.objects.filter(date__lt = today, user = user).order_by('-date')
    tasksRes = []
    for each in tasks:
        tasksRes.append({
            'id':each.id, 
            'task':str(each.task), 
            'sender': str(each.sender), 
            'subject': str(each.subject), 
            'content': str(each.content.encode('utf-8')), 
            'threadID': str(each.threadID), 
            'typeTask': str(each.typeTask), 
            'mailer': str(each.mailer),
            'status':str(each.status), 
            'date': str(each.date),
            'notif': NOTIFICATION_MSG
        })
    return tasksRes

# Get User Profile Info
def profileInfo(request):
    # Output values from the Session Object
    if request.session.has_key('type'):
        user = getUser(email = request.session['email'])
        sett = Settings.objects.get(user = user)
        info = {
            'name' : request.session['name'],
            'email' : request.session['email'],
            'picture' : request.session['picture'],
            'deskNot': sett.browserNotification,
            'timeNot': sett.timeOfNotification.strftime("%H:%M")
        }
        return HttpResponse(json.dumps(info), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Get Settings of User
def settingsGet(request):
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        sett = Settings.objects.get(user = user)
        settRes = {
            'appNot' : sett.appNotification,
            'smsNot' : sett.smsNotification,
            'deskNot' : sett.browserNotification,
            'timeNot' : sett.timeOfNotification.strftime("%I:%M %p"),
            'mob' : sett.mobileForNotification,
            'mobVer' : sett.mobileVerified,
            'emailNo' : sett.noOfMsg,
            'timePer' : sett.timePer
        }               
        return HttpResponse(json.dumps(settRes), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Pass Code Generator
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Get Keywords by User
def keywordsGet(email):
    user = getUser(email)
    try:
        keys = Keywords.objects.filter(user = user).order_by('key')
        keysRes = []
        for each in keys:
            keysRes.append({'id':each.id, 'action':str(each.action), 'key': str(each.key)})
    except Keywords.DoesNotExist:
        keysRes = []
    return json.dumps({"keywords": keysRes})

##################################### 

##################################### Reminders
# Current Day Tasks
def tasks(request):
    if request.session.has_key('type'):
        resp = {'tasks':tasksGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# All Reminders
def reminders(request):
    if request.session.has_key('type'):
        resp = {'tasks':remindersGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# All Missed Reminders
def missed(request):
    if request.session.has_key('type'):
        resp = {'tasks':missedGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Add Task on Current Day
def taskAdd(request):
    # Input: Task
    # Output: All Tasks for Today
    if request.session.has_key('type'):
        resp = {}
        if request.POST.has_key('task'):
            task = request.POST['task'];
            if task.strip() != '':
                user = getUser(request.session['email'])
                today = time.strftime("%Y-%m-%d")
                task = Reminder(user = user, date = today, task = task, status = 'pending', typeTask = 'user', sender = '', subject = '', content = '', mailer = user.login_type, threadID = '')
                task.save()
                tasks = tasksGet(request.session['email'])
                resp = {'done':True,'tasks':tasks}
            else:
                resp = {'done':False,'error':'No Task Provided'}
        else:
            resp = {'done':False,'error':'No Task Provided'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Add Reminder
def reminderAdd(request):
    # Input: Task, Date
    # Output: All Tasks of User
    if request.session.has_key('type'):
        resp = {}
        if request.POST.has_key('task') and request.POST.has_key('date'):
            task = request.POST['task'];
            date = request.POST['date'];
            if task.strip() != '':
                user = getUser(request.session['email'])
                task = Reminder(user = user, date = date, task = task, status = 'pending', typeTask = 'user', sender = '', subject = '', content = '', mailer = user.login_type, threadID = '')
                task.save()
                tasks = remindersGet(request.session['email'])
                resp = {'done':True,'tasks':tasks}
            else:
                resp = {'done':False,'error':'No Date/Reminder Provided'}
        else:
            resp = {'done':False,'error':'No Date/Reminder Provided'}     
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Delete Task of Current Day
def taskDel(request):
    # Input: Task ID
    # Output: All Tasks for Today
    if request.session.has_key('type'):
        task = request.POST['id'];
        task = Reminder.objects.get(id = int(task))
        task.delete()       
        resp = {'tasks':tasksGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Delete All Tasks of Current Day
def taskDelAll(request):
    # Input: None
    # Output: All Tasks for Today
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        today = time.strftime("%Y-%m-%d")
        tasks = Reminder.objects.filter(date = today, user = user)
        for each in tasks:
            each.delete()       
        resp = {'tasks':tasksGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Delete Task
def reminderDel(request):
    # Input: Task ID
    # Output: All Tasks of User
    if request.session.has_key('type'):
        task = request.POST['id'];
        task = Reminder.objects.get(id = int(task))
        task.delete()       
        resp = {'tasks':remindersGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Delete All Tasks of User for a given date
def reminderDelAll(request):
    # Input: Date
    # Output: All Tasks of User
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        date = request.POST['date'];
        tasks = Reminder.objects.filter(date = date, user = user)
        for each in tasks:
            each.delete()       
        resp = {'tasks':remindersGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Delete Task
def missedDel(request):
    # Input: Task ID
    # Output: All Tasks of User
    if request.session.has_key('type'):
        task = request.POST['id'];
        task = Reminder.objects.get(id = int(task))
        task.delete()       
        resp = {'tasks':missedGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Delete All Tasks of User for a given date
def missedDelAll(request):
    # Input: Date
    # Output: All Tasks of User
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        date = request.POST['date'];
        tasks = Reminder.objects.filter(date = date, user = user)
        for each in tasks:
            each.delete()       
        resp = {'tasks':missedGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark Task of User as Completed
def taskCheck(request):
    # Input: Task ID
    # Output: All Tasks for Today
    if request.session.has_key('type'):
        task = request.POST['id'];
        task = Reminder.objects.get(id = int(task))
        task.status = 'done'
        task.save()       
        resp = {'tasks':tasksGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark All Tasks of Current Day as Completed
def taskCheckAll(request):
    # Input: None
    # Output: All Tasks for Today
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        today = time.strftime("%Y-%m-%d")
        tasks = Reminder.objects.filter(date = today, user = user)
        for each in tasks:
            each.status = 'done'
            each.save()       
        resp = {'tasks':tasksGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark Task of User as Completed
def reminderCheck(request):
    # Input: Task ID
    # Output: All Tasks of User
    if request.session.has_key('type'):
        task = request.POST['id'];
        task = Reminder.objects.get(id = int(task))
        task.status = 'done'
        task.save()       
        resp = {'tasks':remindersGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark All Tasks of User as Completed
def reminderCheckAll(request):
    # Input: Date
    # Output: All Tasks of User
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        date = request.POST['date'];
        tasks = Reminder.objects.filter(date = date, user = user)
        for each in tasks:
            each.status = 'done'
            each.save()          
        resp = {'tasks':remindersGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark Task of User as Completed
def missedCheck(request):
    # Input: Task ID
    # Output: All Tasks of User
    if request.session.has_key('type'):
        task = request.POST['id'];
        task = Reminder.objects.get(id = int(task))
        task.status = 'done'
        task.save()       
        resp = {'tasks':missedGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark All Tasks of User as Completed
def missedCheckAll(request):
    # Input: Date
    # Output: All Tasks of User
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        date = request.POST['date'];
        tasks = Reminder.objects.filter(date = date, user = user)
        for each in tasks:
            each.status = 'done'
            each.save()          
        resp = {'tasks':missedGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark Task of Current Day as Pending
def taskUnCheck(request):
    # Input: Task ID
    # Output: All Tasks for Today
    if request.session.has_key('type'):
        task = request.POST['id'];
        task = Reminder.objects.get(id = int(task))
        task.status = 'pending'
        task.save()       
        resp = {'tasks':tasksGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark All Tasks of Current Day as Pending
def taskUnCheckAll(request):
    # Input: None
    # Output: All Tasks for Today
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        today = time.strftime("%Y-%m-%d")
        tasks = Reminder.objects.filter(date = today, user = user)
        for each in tasks:
            each.status = 'pending'
            each.save()       
        resp = {'tasks':tasksGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark Task of User as Pending
def reminderUnCheck(request):
    # Input: Task ID
    # Output: All Tasks for Today
    if request.session.has_key('type'):
        task = request.POST['id'];
        task = Reminder.objects.get(id = int(task))
        task.status = 'pending'
        task.save()       
        resp = {'tasks':remindersGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark All Tasks of User as Pending on a given date
def reminderUnCheckAll(request):
    # Input: Date
    # Output: All Tasks of User
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        date = request.POST['date'];
        tasks = Reminder.objects.filter(date = date, user = user)
        for each in tasks:
            each.status = 'pending'
            each.save()          
        resp = {'tasks':remindersGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark Task of User as Pending
def missedUnCheck(request):
    # Input: Task ID
    # Output: All Tasks for Today
    if request.session.has_key('type'):
        task = request.POST['id'];
        task = Reminder.objects.get(id = int(task))
        task.status = 'pending'
        task.save()       
        resp = {'tasks':missedGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Mark All Tasks of User as Pending on a given date
def missedUnCheckAll(request):
    # Input: Date
    # Output: All Tasks of User
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        date = request.POST['date'];
        tasks = Reminder.objects.filter(date = date, user = user)
        for each in tasks:
            each.status = 'pending'
            each.save()          
        resp = {'tasks':missedGet(request.session['email'])}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Edit Task
def taskEdit(request):
    # Input: Task ID, New Task
    # Output: All Tasks for Today
    if request.session.has_key('type'):
        resp = {}
        if request.POST.has_key('task'):
            idT = request.POST['id'];
            task = request.POST['task'];        
            if task.strip() != '':
                task_obj = Reminder.objects.get(id = int(idT))
                task_obj.task = task
                task_obj.save()
                tasks = tasksGet(request.session['email'])
                resp = {'done':True,'tasks':tasks}
            else:                
                resp = {'done':False,'error':'No Task Provided'}     
        else:
            resp = {'done':False,'error':'No Task Provided'}     
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Edit Task
def reminderEdit(request):
    # Input: Task ID, New Task
    # Output: All Tasks of User
    if request.session.has_key('type'):
        resp = {}
        if request.POST.has_key('task'):
            idT = request.POST['id'];
            task = request.POST['task'];
            if task.strip() != '':
                task_obj = Reminder.objects.get(id = int(idT))
                task_obj.task = task
                task_obj.save()       
                tasks = remindersGet(request.session['email'])
                resp = {'done':True,'tasks':tasks}
            else:
                resp = {'done':False,'error':'No Reminder Provided'}
        else:
            resp = {'done':False,'error':'No Reminder Provided'}     
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

##################################### 

##################################### Settings
# Toggle Mobile App Notification
def appNotToggle(request):
    # Input: None
    # Output: Completion Flag
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        sett = Settings.objects.get(user = user)
        if(sett.appNotification):
            sett.appNotification = False
        else:
            sett.appNotification = True
        sett.save()     
        return HttpResponse(json.dumps({'done':True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Toggle SMS Notification
def smsNotToggle(request):
    # Input: None
    # Output: Completion Flag
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        sett = Settings.objects.get(user = user)
        if(sett.smsNotification):
            sett.smsNotification = False
        else:
            sett.smsNotification = True
        sett.save()     
        return HttpResponse(json.dumps({'done':True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Toggle Browser Notification
def browserNotToggle(request):
    # Input: None
    # Output: Completion Flag
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        sett = Settings.objects.get(user = user)
        if(sett.browserNotification):
            sett.browserNotification = False
        else:
            sett.browserNotification = True
        sett.save()     
        return HttpResponse(json.dumps({'done':True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Update Time of Notification
def timeNotUpdate(request):
    # Input: New Time
    # Output: Completion Flag
    if request.session.has_key('type'):
        if request.POST.has_key('time'):
            user = getUser(request.session['email'])
            sett = Settings.objects.get(user = user)
            timeToUpdate = request.POST['time']
            timeRes = datetime.strptime(timeToUpdate, "%I:%M %p")
            sett.timeOfNotification = timeRes
            sett.save()     
            return HttpResponse(json.dumps({'done':True}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'done':False, 'error': 'Time not provided'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Update Number of Emails to Show
def emailNoUpdate(request):
    # Input: New Number of Emails
    # Output: Completion Flag
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        sett = Settings.objects.get(user = user)
        sett.noOfMsg = request.POST['val']
        sett.save()     
        return HttpResponse(json.dumps({'done':True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Update Time Period of Emails to Show
def timePerUpdate(request):
    # Input: New Time Period
    # Output: Completion Flag
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        sett = Settings.objects.get(user = user)        
        sett.timePer = request.POST['val']
        sett.save()     
        return HttpResponse(json.dumps({'done':True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Update Phone Number of User
def phoneUpdate(request):
    # Input: New Phone Number
    # Output: Completion Flag
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        sett = Settings.objects.get(user = user)        
        sett.mobileForNotification = request.POST['phone']
        now = datetime.now() + timedelta(minutes=10)
        request.session['varCodeTime'] = now.strftime("%Y%m%d%H%M")
        sett.varCodeTime = now
        sett.verCode = id_generator()
        # sendVerCode()
        sett.save()     
        return HttpResponse(json.dumps({'done':True}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Check Verification Code during Phone Number Verification
def varCodeCheck(request):
    # Input: Verification Code
    # Output: Completion Flag
    if request.session.has_key('type'):
        user = getUser(request.session['email'])
        sett = Settings.objects.get(user = user)        
        varCodeTest = request.POST['code']
        now = int((datetime.now()).strftime("%Y%m%d%H%M"))
        checkTime = int(request.session['varCodeTime'])
        if varCodeTest == sett.verCode and now <= checkTime:
            resJ = {'done':True}
            sett.mobileVerified = True
        elif varCodeTest != sett.verCode:
            resJ = {'done':False, 'error': 'Incorrect Verification Code'}
        elif now > checkTime:
            resJ = {'done':False, 'error': 'Verification Code Expired. Check for the new verification code we have sent you for verification'}
            now = datetime.now() + timedelta(minutes=10)
            request.session['varCodeTime'] = now.strftime("%Y%m%d%H%M")
            sett.varCodeTime = now
            sett.verCode = id_generator()
            # sendVerCode()
        sett.save()     
        return HttpResponse(json.dumps(resJ), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

#####################################

##################################### Keywords
# Get All Keywords
def keywordsAllGet(request):
    # Input: None
    # Outout: All Keywords of User
    if request.session.has_key('type'):      
        return HttpResponse(keywordsGet(request.session['email']), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Add keyword
def keywordAdd(request):
    # Input: Key, Action
    # Outout: All Keywords of User
    if request.session.has_key('type'):
        if request.POST.has_key('key') and request.POST.has_key('action'):
            key = request.POST['key'];
            action = request.POST['action'];
            if key.strip() != '' and action.strip() != '':
                user = getUser(request.session['email'])
                keyword = Keywords(user = user, key = key, action = action)
                keyword.save()      
            return HttpResponse(keywordsGet(request.session['email']), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'done':False, 'error': 'Both Fields must be provided'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Delete keyword
def keywordDel(request):
    # Input: Keyword
    # Outout: All Keywords of User
    if request.session.has_key('type'):
        key = request.POST['key'];
        keywords = Keywords.objects.filter(key = key)
        for each in keywords:
            each.delete()        
        return HttpResponse(keywordsGet(request.session['email']), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Delete Action
def keywordActionDel(request):
    # Input: Action ID
    # Outout: All Keywords of User
    if request.session.has_key('type'):
        key = request.POST['id'];
        keyword = Keywords.objects.get(id = int(key))
        keyword.delete()        
        return HttpResponse(keywordsGet(request.session['email']), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Update keyword
def keywordKeyEdit(request):
    # Input: Old Keyword, New Keyword
    # Outout: All Keywords of User
    if request.session.has_key('type'):
        key = request.POST['key'];
        newkey = request.POST['newkey'];
        if newkey.strip() != '':  
            keywords = Keywords.objects.filter(key = key)
            for each in keywords:
                each.key = newkey
                each.save()        
        return HttpResponse(keywordsGet(request.session['email']), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Update Action
def keywordActionEdit(request):
    # Input: Action ID, New Action
    # Outout: All Keywords of User
    if request.session.has_key('type'):
        key = request.POST['id'];
        action = request.POST['action'];
        if action.strip() != '':                
            keyword = Keywords.objects.get(id = int(key))
            keyword.action = action        
            keyword.save()        
        return HttpResponse(keywordsGet(request.session['email']), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

##################################### 

##################################### Email Section
######### To Be done in Future

# def toDateTimeText(str):
#     dateList = str.split(" ")
#     yr = dateList[3]
#     month = dateList[2]
#     date = dateList[1]
#     time = dateList[4]
#     months = {
#         'jan': '01',
#         'feb': '02',
#         'mar': '03',
#         'apr': '04',
#         'may': '05',
#         'jun': '06',
#         'jul': '07',
#         'aug': '08',
#         'sep': '09',
#         'oct': '10',
#         'nov': '11',
#         'dec': '12'
#     }

#     dateText = month + ' ' + date + ' ' + yr
#     timeAc = datetime.strptime(dateText, '%b %d %Y')

#     dateFull = timeAc.strftime('%d %b, %Y')

#     return dateFull

# def getGmailEmail(for_type, mailID, refresh_token, user_email):
#     # Get Access Token
#     url = 'https://accounts.google.com/o/oauth2/token'
#     data = {
#         'grant_type':'refresh_token',
#         'client_id':'520854234186-t0n1oeidnseke2hahepfhkfl7bkc9tou.apps.googleusercontent.com',
#         'client_secret':'KtjgcCb3o2ruq3x5U4H3MUcy',
#         'refresh_token':refresh_token
#     }
#     headers = {
#         'content-type':'application/x-www-form-urlencoded',
#         'accept':'application/json'
#     }
#     response = requests.post(url, data = data, headers = headers)
#     resJ = response.json()
#     access_token = resJ['access_token']

#     url = "https://www.googleapis.com/gmail/v1/users/" + user_email + "/messages/" + mailID
#     payload = {
#         'access_token': access_token
#     }
#     response = requests.get(url, params=payload).json()

#     resJ = {
#         'starred': False,
#         'important': False,
#         'time': "9:45 AM",
#         'subject': "",
#         'files_attch': False
#     }

#     if 'IMPORTANT' in response['labelIds']:
#         resJ['important'] = True

#     if 'STARRED' in response['labelIds']:
#         resJ['starred'] = True

#     for each in response['payload']['headers']:
#         if each['name'] == 'From':
#             if for_type == 'inbox':
#                 resJ['from'] = each['value']
#         elif each['name'] == 'To':
#             if for_type == 'sent':
#                 resJ['to'] = each['value']
#         elif each['name'] == 'Subject':
#             resJ['subject'] = each['value']
#         elif each['name'] == 'Date':
#             resJ['time'] = toDateTimeText(each['value'])    
    
#     return resJ

# def getGmailEmailsInfo(for_type, refresh_token, timePer, noOfMsg, user_email):
#     # Get Access Token
#     url = 'https://accounts.google.com/o/oauth2/token'
#     data = {
#         'grant_type':'refresh_token',
#         'client_id':'520854234186-t0n1oeidnseke2hahepfhkfl7bkc9tou.apps.googleusercontent.com',
#         'client_secret':'KtjgcCb3o2ruq3x5U4H3MUcy',
#         'refresh_token':refresh_token
#     }
#     headers = {
#         'content-type':'application/x-www-form-urlencoded',
#         'accept':'application/json'
#     }
#     response = requests.post(url, data = data, headers = headers)
#     resJ = response.json()
#     access_token = resJ['access_token']

#     # Get Time Interval
#     after = (datetime.now() - timedelta(days=timePer)).strftime("%Y/%m/%d")
#     before = (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d")

#     # Get Emails
#     if for_type == "sent":
#         queryStr = ""
#     else:
#         queryStr = "after:" + after + " before:" + before
#     print queryStr
#     payload = {
#         'access_token': access_token, 
#         'maxResults': 1000000,
#         'q': queryStr,
#         'labelIds': for_type.upper()
#     }
#     url = "https://www.googleapis.com/gmail/v1/users/" + user_email + "/messages"
#     response = requests.get(url, params=payload).json()
#     msgList = response['messages']

#     return {'mails': msgList,'no_of_msg': noOfMsg}

# def getEmail(request):
#     if request.session.has_key('type'):
#         user = User.objects.get(email = request.session['email'])
#         sett = Settings.objects.get(user = user)
#         if(user.login_type == 'gmail'):         
#             refresh_token = user.refresh_token
#             user_email = user.email
#             resJ = getGmailEmail(request.POST['for'], request.POST['mailID'], refresh_token, user_email)
#         return HttpResponse(json.dumps(resJ), content_type="application/json")
#     else:
#         return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# def getEmailsInfo(request):
#     if request.session.has_key('type'):
#         user = User.objects.get(email = request.session['email'])
#         sett = Settings.objects.get(user = user)
#         if(user.login_type == 'gmail'):         
#             refresh_token = user.refresh_token
#             user_email = user.email
#             noOfMsg = sett.noOfMsg
#             timePer = sett.timePer
#             resJ = getGmailEmailsInfo(request.POST['for'], refresh_token, timePer, noOfMsg, user_email)
#         return HttpResponse(json.dumps(resJ), content_type="application/json")
#     else:
#         return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

##################################### 

##################################### Update User Details After Login
def UpdateUser(sendInfo):
    try:
        userSearch = User.objects.get(email = sendInfo['email'])
        userSearch.name = sendInfo['name']
        userSearch.email = sendInfo['email']
        userSearch.picture = sendInfo['picture']
        userSearch.login_type = sendInfo['login_type']
        userSearch.save()
    except User.DoesNotExist:
        user = User(name = sendInfo['name'], email = sendInfo['email'], picture = sendInfo['picture'], refresh_token = sendInfo['refresh_token'], login_type = sendInfo['login_type'])
        user.save()
        user = User.objects.get(email = sendInfo['email'])
        sett = Settings(user = user, smsNotification = False, appNotification = False, browserNotification = False, mobileForNotification = 99999999999, timePer = 5, noOfMsg = 50)
        sett.save()
        
##################################### 

##################################### Plugin Helpers
# CLean Message
def cleanContent(content):
    
    textInp=content.replace('\t','').replace('\n','')
    # txt = textInp
    txt = textInp.encode('utf-8')
    main_txt=""
    
    sentInd = txt.find("wrote:")
    frwdInd = txt.find("---------- Forwarded message ----------")
    txt90=""
    txt91=""
    sent = False
    frwd = False
    checkSent = False
    checkFrwd = False
    if sentInd != -1:
        sent = True
    if frwdInd != -1:
        frwd = True
    if sent and frwd:
           
        if sentInd < frwdInd:
            txt_find1=re.search(r"(.*?)(On [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{1,2})(.*?)wrote:",txt,re.M)
            checkSent = True
            if txt_find1 is not None:

                txt90=txt_find1.group(1)
                main_txt=txt_find1.group(1)
                txt91=txt_find1.group(0)
        else:
            txt_find1=re.search(r"(---------- Forwarded message ----------(.*?)From:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)To:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?))?(.*?)On [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{1,2}(.*?)wrote:",txt,re.M)
            checkFrwd = True
            if txt_find1 is not None:
                txt90=txt_find1.group(12)
                main_txt=txt_find1.group(12)
                txt91=txt_find1.group(0)
    elif sent:
        checkSent = True
        txt_find1=re.search(r"(.*?)(On [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{1,2})(.*?)wrote:",txt,re.M)
        if txt_find1 is not None:
            txt90=txt_find1.group(1)
            main_txt=txt_find1.group(1)
            txt91=txt_find1.group(0)
        # print txt90

    elif frwd:
        checkFrwd =True
        txt_find1=re.search(r"(---------- Forwarded message ----------(.*?)From:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)(.*?)To:(.*?)([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?))?(.*)",txt,re.M)
        if txt_find1 is not None:
            txt90=txt_find1.group(11)
            main_txt=txt_find1.group(11)
            txt91=txt_find1.group(0)
    else:
        txt90=txt
        main_txt=txt
        txt91=txt

    return main_txt

# Message Info
def getGmailEmailsInfo(refresh_token, user_email, threadID):
    # Get Access Token
    url = 'https://accounts.google.com/o/oauth2/token'
    data = {
        'grant_type':'refresh_token',
        'client_id':'529425540533-b3gvjh0sor2rol0oetdhvkvdp4radmrh.apps.googleusercontent.com',
        'client_secret':'iDFfL3Vfrxg81ZAxa8aDesVb',
        'refresh_token':refresh_token
    }
    headers = {
        'content-type':'application/x-www-form-urlencoded',
        'accept':'application/json'
    }
    response = requests.post(url, data = data, headers = headers)
    resJ = response.json()
    access_token = resJ['access_token']
    payload = {
        'access_token': access_token
    }
    threadUrl = 'https://www.googleapis.com/gmail/v1/users/'+user_email+'/threads/'+threadID
    response = requests.get(threadUrl, params=payload).json()
    messageList = []
    for each in response['messages']:
        msgID = each['id']
        headers = each['payload']['headers']
        fromPerson = ''
        subject = ''
        content = str(each['snippet'])
        
        if each['payload']['body'].has_key('data'):
            raw_email_string = str(each['payload']['body']['data'])
        elif each['payload']['parts'][0]['body'].has_key('data'):
            raw_email_string = str(each['payload']['parts'][0]['body']['data'])
        elif each['payload']['parts'][0]['parts'][0]['body'].has_key('data'):
            raw_email_string = str(each['payload']['parts'][0]['parts'][0]['body']['data'])
        else:
            raw_email_string = str(each['payload']['parts'][0]['parts'][0]['parts'][0]['body']['data'])

        contentDec = base64.urlsafe_b64decode(raw_email_string.encode('ASCII'))
        # Cleaned Content
        cleanContentText = cleanContent(contentDec)

        for head in headers:
            if head['name'] == 'From':
                fromPerson = str(head['value'])
            if head['name'] == 'Subject':
                subject = str(head['value'])

        messageInfo = {
            'sender': fromPerson,
            'subject': subject,
            'content': contentDec,
            'cleanContent': cleanContentText,
            'message_id': msgID,
            'threadID': threadID,
            'remSugs': None,
            'remSugNo': 0,
            'remSug': False,
            'small': True
        }

        # print messageInfo
        messageList.append(messageInfo)
    
    return {'messages': messageList}

# Message Parsing
def getRems(message, messageCleaned, subject,sender,keywords):

    remsInp = textproc.getRemsTextProc(message, keywords)

    rems = []
    for each in remsInp:
        if each['id'] != 0:
            remData = {
                'id': each['id'],
                'rem': each['suggest']
            }
            reminders = []
            if isinstance(each['reminders'], basestring):
                reminders = literal_eval(each['reminders'])
            else:
                reminders = each['reminders']
            if len(reminders) > 0:
                remData['date'] = reminders[0].split('-')[2] + '-' + reminders[0].split('-')[1] + '-' + reminders[0].split('-')[0]
            else:
                remData['date'] = ''
            if each['flag'] == 1:
                remData['type'] = 'user'
            else:
                remData['type'] = 'system'
            rems.append(remData)

    return rems

##################################### 

##################################### Plugin
# Get Message List
def getMessageList(request):
    if request.session.has_key('type'):
        user = getUser(email = request.session['email'])
        sett = Settings.objects.get(user = user)
        if(user.login_type == 'gmail'):         
            refresh_token = user.refresh_token
            user_email = user.email
            threadID = request.POST['threadID']
            resJ = getGmailEmailsInfo(refresh_token, user_email, threadID)
        return HttpResponse(json.dumps(resJ), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Check Message Text
def checkMessageText(request):
    if request.session.has_key('type'):
        user = getUser(email = request.session['email'])
        keywords = keywordsGetPlugin(user)
        message = request.POST['message'];
        messageCleaned = request.POST['cleanContent'];
        subject = request.POST['subject'];
        sender = request.POST['sender'];
        respObj = getRems(message,messageCleaned,subject,sender,keywords)
        resp = {'done':True,'rems': respObj}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

# Save Reminders
def messageSaveRems(request):
    if request.session.has_key('type'):
        user = getUser(email = request.session['email'])
        rems = request.POST['rems'];
        rems = rems.encode("utf-8")
        rems = literal_eval(rems)
        notDetEn = request.POST['notDetEn'];
        noti = request.POST['notDetNot'];
        date = request.POST['notDetDate'];
        email = request.POST['notDetEmail'];
        threadID = request.POST['threadID'];
        
        try:
            for each in rems:
                dateEnter = each['date'].split('-')[2] + '-' + each['date'].split('-')[1] + '-' + each['date'].split('-')[0]
                task = Reminder(user = user, date = dateEnter, task = each['rem'], typeTask = 'mailer', mailer = user.login_type, sender = each['sender'], subject = each['subject'], content = each['content'], threadID = each['threadID'], status = 'pending')
                task.save()
            if notDetEn:
                dateEnter = date.split('-')[2] + '-' + date.split('-')[1] + '-' + date.split('-')[0]
                newNot = Notification(user = user, email = email, message = noti, date = dateEnter, threadID = threadID)
                newNot.save()
            resp = {'done':True}
        except Exception, e:
            print e
            resp = {'done':False, 'error': 'Note: Please Add the Date for each Reminder.if problem persists kindly refresh or try again )'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'error':'Invalid Session'}), content_type="application/json")

#####################################

##################################### Schedulers

# Daily Reminder
def dailyRem(request):
    startDailyReminder()
    return HttpResponse(json.dumps({}), content_type="application/json")

# Upcoming Reminder
def upcomingRem(request):
    startUpcomingReminder()
    return HttpResponse(json.dumps({}), content_type="application/json")

# Missed Reminder
def missedRem(request):
    startMissedReminder()
    return HttpResponse(json.dumps({}), content_type="application/json")

# Deadline Reminder
def deadlineRem(request):
    startDeadlineReminder()
    return HttpResponse(json.dumps({}), content_type="application/json")

#####################################