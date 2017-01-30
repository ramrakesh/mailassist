from fabric.api import run

def deployherogit():
   run('pip freeze > requirements.txt')
   run('git add .')
   print("enter your git commit comment: ")
   comment = raw_input()
   run('git commit -am "%s"' % comment) 
   run('git push -u origin master')
   