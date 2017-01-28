# import scheduler
import time
from models import User, Settings, Reminder, Keywords, Notification
import json
import datetime
import requests

import base64
from email.mime.text import MIMEText
import mimetypes
import os

import smtplib

from apiclient import errors

from .settings import redirectHelper

##################################### Helpers

HOMEPAGE_LINK = redirectHelper() + 'user/#/'
MISSED_LINK = redirectHelper() + 'user/#/history'

# Get All Reminders
def getDailyReminderAllReminders(today,nextSeven):
    remindersGet = Reminder.objects.filter(date__gte = today, date__lte = nextSeven).order_by('date')
    reminders = []
    for each in remindersGet:
        if str(each.status) == 'pending':
            # us = User.objects.get(user = each.user)
            reminders.append({
                'task': str(each.task),
                'date': str(each.date),
                'user': str(each.user.email)
            })
    return reminders

def getUpcomingReminderAllReminders(nextMonth):
    remindersGet = Reminder.objects.filter(date__gte = nextMonth).order_by('date')
    reminders = []
    for each in remindersGet:
        if str(each.status) == 'pending':
            # us = User.objects.get(user = each.user)
            reminders.append({
                'task': str(each.task),
                'date': str(each.date),
                'user': str(each.user.email)
            })
    return reminders

def getMissedReminderAllReminders(lastDay):
    remindersGet = Reminder.objects.filter(date = lastDay).order_by('date')
    reminders = []
    for each in remindersGet:
        if str(each.status) == 'pending':
            # us = User.objects.get(user = each.user)
            reminders.append({
                'task': str(each.task),
                'user': str(each.user.email)
            })
    return reminders

# Get All Notifications
def getNotifications(lastDay):
    notificationsGet = Notification.objects.filter(date = lastDay).order_by('date')
    notifications = []
    for each in notificationsGet:
        
        # us = User.objects.get(user = each.user)
        notifications.append({
            'user': str(each.user.email),
            'email': str(each.email),
            'message': str(each.message)
        })
    return notifications

# Check Valid Date Diff (Weeks: 2)
def validDate(today,date):
    today = datetime.datetime.strptime(today,"%Y-%m-%d")
    date = datetime.datetime.strptime(date,"%Y-%m-%d")
    checkDate = date
    while True:
        checkDate = checkDate - datetime.timedelta(weeks=2)
        if checkDate == today:
            return True
        elif checkDate < today:
            return False    
    return False

# Filter Upcoming Reminders
def filterUpcomingReminders(today, reminders):
    filteredRems = []
    for each in reminders:
        if validDate(today,each['date']):
            filteredRems.append({
                'task': each['task'],
                'date': each['date'],
                'user': each['user']
            })
    return filteredRems

# Get Today Reminders
def getDailyReminderTodayReminder(reminders, today):
    todayReminders = []
    for each in reminders:
        if each['date'] == today:
            todayReminders.append({
                'task': each['task'],
                'date': each['date'],
                'user': each['user']
            })
    return todayReminders

# Get upcoming Reminders
def getDailyReminderUpcomingReminder(reminders, today):
    upcomingReminders = []
    for each in reminders:
        if each['date'] != today:
            upcomingReminders.append({
                'task': each['task'],
                'date': each['date'],
                'user': each['user']
            })
    return upcomingReminders

# Get User/Reminder List
def getDailyReminderUserReminderList(todayReminders,upcomingReminders):
    usersRems = {}
    for each in todayReminders:
        if not usersRems.has_key(each['user']):
            usersRems[each['user']] = {
                'today': [],
                'upcoming':{}
            }
    for each in upcomingReminders:
        if not usersRems.has_key(each['user']):
            usersRems[each['user']] = {
                'today': [],
                'upcoming':{}
            }
    for each in upcomingReminders:
        if not usersRems[each['user']]['upcoming'].has_key(each['date']):
            usersRems[each['user']]['upcoming'][each['date']] = []
    for each in todayReminders:
        usersRems[each['user']]['today'].append(each['task'])
    for each in upcomingReminders:
        usersRems[each['user']]['upcoming'][each['date']].append(each['task'])
    return usersRems

def getUpcomingReminderUserReminderList(reminders):
    usersRems = {}
    for each in reminders:
        if not usersRems.has_key(each['user']):
            usersRems[each['user']] = {}
    for each in reminders:
        if not usersRems[each['user']].has_key(each['date']):
            usersRems[each['user']][each['date']] = []
    for each in reminders:
        usersRems[each['user']][each['date']].append(each['task'])
    return usersRems

def getMissedReminderUserReminderList(reminders):
    usersRems = {}
    for each in reminders:
        if not usersRems.has_key(each['user']):
            usersRems[each['user']] = []
    for each in reminders:
        usersRems[each['user']].append(each['task'])
    return usersRems

# Get Upcoming Msg Count
def upcomingMsgCount(upcomingMsgs):
    count = 0
    for each in upcomingMsgs:
        count = count + len(upcomingMsgs[each])
    return count

# Sort Dates
def sortDates(datesDict):
    sortedDates = []
    for each in datesDict:
        sortedDates.append(each)
    sortedDates.sort()
    # print sortedDates
    return sortedDates

# Get Message List
def getDailyReminderEmailList(usersRems):
    emailsList = {}
    for user in usersRems:
        email = user
        
        todayMsgs = usersRems[user]['today']
        upcomingMsgs = usersRems[user]['upcoming']
        todayLen = len(todayMsgs)
        upcomingLen = upcomingMsgCount(upcomingMsgs)
        subject = ''
        if todayLen == 0:
            subject = 'MailAssist: You have no tasks for today'
        else:
            subject = 'MailAssist: You have ' + str(todayLen) + ' tasks for today'
        userDet = User.objects.get(email = email)
        msgWrapStart = ''
        welcomeMsg = 'Hello ' + str(userDet.name) + '!\n\n'
        todayMsgApp = ''
        if todayLen == 0:
            todayMsgApp = 'You have no tasks for today. \n\n'
        else:
            todayMsgApp = 'Reminders of your tasks to be completed today.\n\n'
            count = 1
            for each in todayMsgs:
                todayMsgApp = todayMsgApp + '\tTask #' + str(count) + ': ' + each + '\n'
                count = count + 1
            todayMsgApp = todayMsgApp + '\n\n'
        upcomingMsgApp = ''
        if upcomingLen != 0:
            upcomingMsgApp = 'Upcoming tasks: \n\n'
            sortedDates = sortDates(upcomingMsgs)
            for each in sortedDates:
                dt = each
                dtShw = dt.split('-')[2] + '/' + dt.split('-')[1] + '/' + dt.split('-')[0]
                upcomingMsgApp = upcomingMsgApp + '\tDate: ' + dtShw + '\n\n'
                    
                count = 1
                for tsk in upcomingMsgs[dt]:
                    upcomingMsgApp = upcomingMsgApp + '\t\tTask #' + str(count) + ': ' + tsk + '\n'
                    count = count + 1
                upcomingMsgApp = upcomingMsgApp + '\n\n'
        linkMsg = '--- MailAssist'
        msgWrapEnd = ''
        finalMsg = msgWrapStart + welcomeMsg + todayMsgApp + upcomingMsgApp + linkMsg + msgWrapEnd
        if todayLen != 0:
            emailsList[email] = {
                'subject': subject,
                'message': finalMsg
            }
    # print emailsList
    return emailsList

def getUpcomingReminderEmailList(usersRems):
    emailsList = {}
    for user in usersRems:
        email = user
        userDet = User.objects.get(email = email)
        sortedDates = sortDates(usersRems[user])
        subject = 'MailAssist: Upcoming Tasks'
        dt = sortedDates[0]
        dtShw = dt.split('-')[2] + '/' + dt.split('-')[1] + '/' + dt.split('-')[0]
        welcomeMsg = 'Hello ' + str(userDet.name) + '!\n\nReminder of the upcoming tasks.\n\n'
        upcomingMsgApp = ''        
        count = 1
        for tsk in usersRems[user][dt]:
            upcomingMsgApp = upcomingMsgApp + '\tTask #' + str(count) + ': ' + tsk + '\n'
            count = count + 1
        upcomingMsgApp = upcomingMsgApp + '\n\n'
        linkMsg = '--- MailAssist'
        finalMsg = welcomeMsg + upcomingMsgApp + linkMsg
        emailsList[email] = {
            'subject': subject,
            'message': finalMsg
        }
    return emailsList

def getMissedReminderEmailList(usersRems):
    emailsList = {}
    for user in usersRems:
        email = user
        userDet = User.objects.get(email = email)
        lastDayMsgs = usersRems[user]
        lastDayLen = len(lastDayMsgs)
        subject = 'MailAssist: You have left ' + str(lastDayLen) + ' tasks yesterday'
        welcomeMsg = 'Hello ' + str(userDet.name) + '!\n\nReminders of the tasks that you have left yesterday.\n\n'
        MsgApp = ''        
        count = 1
        for tsk in lastDayMsgs:
            MsgApp = MsgApp + '\tTask #' + str(count) + ': ' + tsk + '\n'
            count = count + 1
        MsgApp = MsgApp + '\n\n'
        linkMsg = '--- MailAssist'
        finalMsg = welcomeMsg + MsgApp + linkMsg
        if lastDayLen != 0:
            emailsList[email] = {
                'subject': subject,
                'message': finalMsg
            }
    return emailsList

def getdeadlineNotificationEmailList(notifications):
    emailsList = []
    for each in notifications:
        sender = each['user']
        reciepent = each['email']
        subject = 'MailAssist: Regarding status of your query'
        MsgApp = each['message'] + '\n\n--- MailAssist' 
        emailsList.append({
            'subject': subject,
            'message': MsgApp,
            'sender': sender,
            'reciepent': reciepent
        })
    return emailsList

# Send Emails
def sendEmails(emailsList):
    for each in emailsList:
        email = each
        user = User.objects.get(email = email)
        refresh_token = user.refresh_token
        # print refresh_token
        url = 'https://accounts.google.com/o/oauth2/token'
        data = {
            'grant_type':'refresh_token',
            'client_id':'529425540533-b3gvjh0sor2rol0oetdhvkvdp4radmrh.apps.googleusercontent.com',
            'client_secret':'iDFfL3Vfrxg81ZAxa8aDesVb',
            'refresh_token': refresh_token
        }
        headers = {
            'content-type':'application/x-www-form-urlencoded',
            'accept':'application/json'
        }
        response = requests.post(url, data = data, headers = headers)
        resJ = response.json()
        access_token = resJ['access_token']
        
        # print emailsList[each]['message']

        message = MIMEText(emailsList[each]['message'])
        message['to'] = email
        message['from'] = email
        message['subject'] = emailsList[each]['subject']
        message['content-type'] = 'text/html; charset=utf-8'
        message['content-transfer-encoding'] = 'quoted-printable'
        finalMsg = base64.urlsafe_b64encode(message.as_string())

        url = "https://www.googleapis.com/gmail/v1/users/"+email+"/messages/send?access_token=" + access_token
        data = {
            'raw': finalMsg
        }
        response = requests.post(url, data = json.dumps(data), headers={'Content-Type': 'application/json'}).json()

def sendNotificationEmails(emailsList):
    
    authCodes = {}
    
    for each in emailsList:
        sender = each['sender']
        reciepent = each['reciepent']
        subject = each['subject']
        MsgApp = each['message']
        user = User.objects.get(email = sender)
        if not authCodes.has_key(sender):
            refresh_token = user.refresh_token
            url = 'https://accounts.google.com/o/oauth2/token'
            data = {
                'grant_type':'refresh_token',
                'client_id':'529425540533-b3gvjh0sor2rol0oetdhvkvdp4radmrh.apps.googleusercontent.com',
                'client_secret':'iDFfL3Vfrxg81ZAxa8aDesVb',
                'refresh_token': refresh_token
            }
            headers = {
                'content-type':'application/x-www-form-urlencoded',
                'accept':'application/json'
            }
            response = requests.post(url, data = data, headers = headers)
            resJ = response.json()
            access_token = resJ['access_token']
            authCodes[sender] = access_token
        else:
            access_token = authCodes[sender]
        
        message = MIMEText(MsgApp)
        message['To'] = reciepent
        message['From'] = sender
        message['Subject'] = subject
        message['content-type'] = 'text/html; charset=utf-8'
        message['content-transfer-encoding'] = 'quoted-printable'
        finalMsg = base64.urlsafe_b64encode(message.as_string())

        # print '##############################'
        # print finalMsg
        # print MsgApp
        # print sender
        # print reciepent
        # print '##############################'

        url = "https://www.googleapis.com/gmail/v1/users/"+sender+"/messages/send?access_token=" + access_token
        data = {
            'raw': finalMsg
        }
        response = requests.post(url, data = json.dumps(data), headers={'Content-Type': 'application/json'}).json()

        print response

#####################################

##################################### Schedulers

# Today/Upcoming Scheduler
def dailyReminder():

    # Get Dates
    today = datetime.datetime.today()
    nextSeven = today + datetime.timedelta(days=7)

    today = today.strftime("%Y-%m-%d")
    nextSeven = nextSeven.strftime("%Y-%m-%d")

    # Get Reminders
    reminders = getDailyReminderAllReminders(today,nextSeven)
    todayReminders = getDailyReminderTodayReminder(reminders, today)
    upcomingReminders = getDailyReminderUpcomingReminder(reminders, today)

    # User/Reminders List
    usersRems = getDailyReminderUserReminderList(todayReminders,upcomingReminders)
    
    # Message List
    emailsList = getDailyReminderEmailList(usersRems)

    # Send Emails
    sendEmails(emailsList)

# Upcoming Reminder
def upcomingReminder():

    # Get Dates
    today = datetime.datetime.today()
    nextMonth = today + datetime.timedelta(weeks=4)

    today = today.strftime("%Y-%m-%d")
    nextMonth = nextMonth.strftime("%Y-%m-%d")

    # Get Reminders
    reminders = getUpcomingReminderAllReminders(nextMonth)
    
    # Filter Reminder
    reminders = filterUpcomingReminders(today, reminders)

    # User/Reminders List
    usersRems = getUpcomingReminderUserReminderList(reminders)
    
    # Message List
    emailsList = getUpcomingReminderEmailList(usersRems)
    
    # Send Emails
    sendEmails(emailsList)

# Missed Reminder
def missedReminder():

    # Get Dates
    today = datetime.datetime.today()
    lastDay = today - datetime.timedelta(days = 1)

    today = today.strftime("%Y-%m-%d")
    lastDay = lastDay.strftime("%Y-%m-%d")

    # Get Reminders
    reminders = getMissedReminderAllReminders(lastDay)
    
    # User/Reminders List
    usersRems = getMissedReminderUserReminderList(reminders)

    # Message List
    emailsList = getMissedReminderEmailList(usersRems)
    
    # Send Emails
    sendEmails(emailsList)

# Deadline Notification
def deadlineReminder():

    # Get Dates
    today = datetime.datetime.today()
    lastDay = today - datetime.timedelta(days = 1)

    today = today.strftime("%Y-%m-%d")
    lastDay = lastDay.strftime("%Y-%m-%d")

    # Get Notifications
    notifications = getNotifications(lastDay)
    
    # Message List
    emailsList = getdeadlineNotificationEmailList(notifications)

    # Send Emails
    sendNotificationEmails(emailsList)

#####################################