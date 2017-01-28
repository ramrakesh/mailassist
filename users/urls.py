from django.conf.urls import url
import tasks

from . import views, api

urlpatterns = [
    
    ##################################### Index Page
	url(r'^$', views.index, name = 'index'),

    ##################################### Templates
	url(r'^MailAssistUserTemplates/index-template.html$', views.mainView, name = 'indexView'),
    url(r'^MailAssistUserTemplates/header-template.html$', views.header, name = 'header'),
    url(r'^MailAssistUserTemplates/footer-template.html$', views.footer, name = 'footer'),
    url(r'^MailAssistUserTemplates/side-nav-template.html$', views.sideNav, name = 'sideNav'),
    url(r'^MailAssistUserTemplates/missed-template.html$', views.missed, name = 'missed'),
    # url(r'^MailAssistUserTemplates/inbox-template.html$', views.inbox, name = 'inbox'),
    # url(r'^MailAssistUserTemplates/sent-template.html$', views.sent, name = 'sent'),
    url(r'^MailAssistUserTemplates/preferences-template.html$', views.preferences, name = 'preferences'),
    url(r'^MailAssistUserTemplates/keywords-template.html$', views.keywords, name = 'keywords'),
    url(r'^MailAssistUserTemplates/reminders-template.html$', views.reminder, name = 'reminder'),
    # url(r'^MailAssistUserTemplates/compose-template.html$', views.compose, name = 'compose'),
    
    ##################################### APIs
    # Basic
    url(r'^profile-info$', api.profileInfo, name = 'profileInfo'),
    
    # Tasks and Reminders
    url(r'^tasks$', api.tasks, name = 'tasks'),
    url(r'^tasks/add$', api.taskAdd, name = 'tasksAdd'),
    url(r'^tasks/del$', api.taskDel, name = 'tasksDel'),
    url(r'^tasks/del/all$', api.taskDelAll, name = 'tasksDelAll'),
    url(r'^tasks/check$', api.taskCheck, name = 'tasksCheck'),
    url(r'^tasks/check/all$', api.taskCheckAll, name = 'tasksCheckAll'),
    url(r'^tasks/uncheck$', api.taskUnCheck, name = 'tasksUnCheck'),
    url(r'^tasks/uncheck/all$', api.taskUnCheckAll, name = 'tasksUnCheckAll'),
    url(r'^tasks/edit$', api.taskEdit, name = 'tasksEdit'),
    url(r'^reminders$', api.reminders, name = 'reminders'),
    url(r'^reminders/add$', api.reminderAdd, name = 'reminderAdd'),
    url(r'^reminders/del$', api.reminderDel, name = 'reminderDel'),
    url(r'^reminders/del/all$', api.reminderDelAll, name = 'reminderDelAll'),
    url(r'^reminders/check$', api.reminderCheck, name = 'reminderCheck'),
    url(r'^reminders/check/all$', api.reminderCheckAll, name = 'reminderCheckAll'),
    url(r'^reminders/uncheck$', api.reminderUnCheck, name = 'reminderUnCheck'),
    url(r'^reminders/uncheck/all$', api.reminderUnCheckAll, name = 'reminderUnCheckAll'),
    url(r'^reminders/edit$', api.reminderEdit, name = 'reminderEdit'),
    url(r'^missed$', api.missed, name = 'missed'),
    url(r'^missed/del$', api.missedDel, name = 'missedDel'),
    url(r'^missed/del/all$', api.missedDelAll, name = 'missedDelAll'),
    url(r'^missed/check$', api.missedCheck, name = 'missedCheck'),
    url(r'^missed/check/all$', api.missedCheckAll, name = 'missedCheckAll'),
    url(r'^missed/uncheck$', api.missedUnCheck, name = 'missedUnCheck'),
    url(r'^missed/uncheck/all$', api.missedUnCheckAll, name = 'missedUnCheckAll'),
    
    # Keywords
    url(r'^keywords/get$', api.keywordsAllGet, name = 'keywordsAllGet'),
    url(r'^keywords/add$', api.keywordAdd, name = 'keywordAdd'),
    url(r'^keywords/del$', api.keywordDel, name = 'keywordDel'),
    url(r'^keywords/action/del$', api.keywordActionDel, name = 'keywordActionDel'),
    url(r'^keywords/key/edit$', api.keywordKeyEdit, name = 'keywordKeyEdit'),
    url(r'^keywords/action/edit$', api.keywordActionEdit, name = 'keywordActionEdit'),

    # Settings
    url(r'^settings/get$', api.settingsGet, name = 'settingsGet'),
    url(r'^settings/appNot/toggle$', api.appNotToggle, name = 'appNotToggle'),
    url(r'^settings/smsNot/toggle$', api.smsNotToggle, name = 'smsNotToggle'),
    url(r'^settings/browserNot/toggle$', api.browserNotToggle, name = 'browserNotToggle'),
    url(r'^settings/update-time-of-notification$', api.timeNotUpdate, name = 'timeNotUpdate'),
    url(r'^settings/update-number-of-email$', api.emailNoUpdate, name = 'emailNoUpdate'),
    url(r'^settings/update-time-period$', api.timePerUpdate, name = 'timePerUpdate'),
    url(r'^settings/update-phone$', api.phoneUpdate, name = 'phoneUpdate'),
    url(r'^settings/update-phone-verification$', api.varCodeCheck, name = 'varCodeCheck'),

    # Plugin
    url(r'^plugin/message/get-message-list$', api.getMessageList, name = 'getMessageList'),
    url(r'^plugin/message/check-text$', api.checkMessageText, name = 'checkMessageText'),
    url(r'^plugin/message/save-rems$', api.messageSaveRems, name = 'messageSaveRems'),

    # url(r'^mails/get$', api.getEmail, name = 'getEmail'),
    # url(r'^mails/info$', api.getEmailsInfo, name = 'getEmailsInfo')

    # Scheduler
    url(r'^schedules$', views.sched, name = 'sched'),
    url(r'^scheduler/daily-reminder$', api.dailyRem, name = 'dailyRem'),
    url(r'^scheduler/upcoming-reminder$', api.upcomingRem, name = 'upcomingRem'),
    url(r'^scheduler/missed-reminder$', api.missedRem, name = 'missedRem'),
    url(r'^scheduler/deadline-reminder$', api.deadlineRem, name = 'deadlineRem')

]