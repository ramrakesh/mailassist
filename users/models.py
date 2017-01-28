from django.db import models

# User Model
class User(models.Model):
	name = models.CharField(max_length = 100)
	email = models.EmailField(max_length = 254)
	refresh_token = models.CharField(max_length = 254)
	picture = models.TextField()
	login_type = models.CharField(max_length = 50)

# Notification Model
class Notification(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	threadID = models.TextField()
	date = models.DateField(auto_now = False, auto_now_add = False)
	message = models.TextField()
	email = models.EmailField(max_length = 254)

# User Reminder Model
class Reminder(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	typeTask =  models.CharField(max_length = 10)
	task = models.TextField()
	date = models.DateField(auto_now = False, auto_now_add = False)
	sender = models.TextField()
	subject = models.TextField()
	content = models.TextField()
	mailer =  models.CharField(max_length = 10)
	threadID = models.TextField()
	status = models.CharField(max_length = 10)

# User Settings Model
class Settings(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	smsNotification = models.BooleanField(default = False)
	appNotification = models.BooleanField(default = False)
	browserNotification = models.BooleanField(default = False)
	mobileForNotification = models.BigIntegerField(default = 0000000000)
	mobileVerified = models.BooleanField(default = False)
	timePer = models.IntegerField(default = 5)
	noOfMsg = models.IntegerField(default = 50)
	verCode = models.CharField(max_length = 50)
	varCodeTime = models.DateTimeField(auto_now = False, auto_now_add = True)
	timeOfNotification = models.TimeField(auto_now = False, auto_now_add = True)

# User Keywords Model
class Keywords(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	key = models.CharField(max_length = 50)
	action = models.TextField()

# Admin Schedules
class DailySchedules(models.Model):
	name = models.CharField(max_length = 50)
	date = models.DateField(auto_now = False, auto_now_add = False)
	status = models.CharField(max_length = 10)
