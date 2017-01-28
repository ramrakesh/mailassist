# from celery.task import PeriodicTask
# from datetime import timedelta

# import schedulers

# class DailyReminderStart(PeriodicTask):
#     run_every = timedelta(seconds=5)

#     def run(self, **kwargs):
#         schedulers.dailyReminder()

# dailyReminderStart()