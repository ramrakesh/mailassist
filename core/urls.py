from django.conf.urls import url

from . import views, api

urlpatterns = [
	
	##################################### Index Page
	url(r'^$', views.index, name = 'index'),
	
	##################################### Templates
	url(r'^MailAssistCoreTemplates/index-template.html$', views.mainView, name = 'indexView'),
	url(r'^MailAssistCoreTemplates/header-template.html$', views.header, name = 'header'),
	url(r'^MailAssistCoreTemplates/footer-template.html$', views.footer, name = 'footer'),
	url(r'^MailAssistCoreTemplates/plugin-template.html$', views.plugin, name = 'plugin'),
	url(r'^MailAssistCoreTemplates/mobile-template.html$', views.mobile, name = 'mobile'),
	url(r'^MailAssistCoreTemplates/page-not-found.html$', views.notfound, name = 'not-found'),

	##################################### Login
	url(r'^gmail$', api.gmailLogin, name = 'gmailLogin'), # Login with Gmail Step 1
	url(r'^oauth2callback$', api.gmailLoginStep2, name = 'gmailLogin'), # Login with Gmail Step 2

	##################################### Logout
	url(r'^logout$', api.logout, name = 'logout'),

	##################################### Plugin
	url(r'^plugin/check-session$', api.checkPluginSession, name = 'checkPluginSession')
]