from celery import app
import schedulers

@app.task
def startDailyReminder():
    schedulers.dailyReminder()

@app.task
def startUpcomingReminder():
	schedulers.upcomingReminder()

@app.task
def startMissedReminder():
	schedulers.missedReminder()

@app.task
def startDeadlineReminder():
	schedulers.deadlineReminder()