from fabric.api import run,env

def deployheroku():
   run('pip freeze > requirements.txt')
   run('git add .')
   print("enter your git commit comment: ")
   comment = raw_input()
   run('git commit -am "%s"' % comment)
   run('heroku maintenance:on')
   run('heroku config:set DISABLE_COLLECTSTATIC=0')
   run('git push heroku master')
   run('heroku run python manage.py makemigrations')
   run('heroku run python manage.py migrate')
   run('heroku config:unset DISABLE_COLLECTSTATIC')
   run('heroku run python manage.py collectstatic')
   run('git push -u origin master')
   run('heroku logs')
   run('heroku maintenance:off')