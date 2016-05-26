# -*- coding: utf-8 -*-
from fabric.api import *

PRODUCTION = 'digger-eth.bethania'
SENCHA = '/opt/SenchaSDKTools-1.2.3'


def production():
  env.hosts = [ PRODUCTION ]
  env.repo = 'semurg'
  env.parent = 'origin'
  env.branch = 'master'
  env.home = '/home/drseergio'
  env.www = '/var/www/semurg'


def makecss():
  local('git rm -f core/static/resources/images/icons-*png;'
        'cd core/static/resources/sass;'
        'compass compile semurg.scss;'
        'cd -;'
        'sed -i -e \'s:/\.\.:..:g\' -e \'s/background-position:0 -[0-9]*px/& !important/ig\' core/static/resources/css/semurg.css;'
        'git add core/static/resources/images/icons-*png;')


def makejs():
  local('cd core/static;'
        'PATH="${PATH}:%(SENCHA)s/appbuilder/:%(SENCHA)s/command:%(SENCHA)s" sencha create jsb -a build.html -p app.jsb3;'
        'PATH="${PATH}:%(SENCHA)s/appbuilder/:%(SENCHA)s/jsbuilder:%(SENCHA)s/command:%(SENCHA)s" sencha build -p app.jsb3 -d .' % {'SENCHA': SENCHA})


def pushpull():
  local('git push production')
  local('cd core/static;'
        'PATH="${PATH}:%(SENCHA)s/appbuilder/:%(SENCHA)s/command:%(SENCHA)s" sencha create jsb -a build.html -p app.jsb3;'
        'PATH="${PATH}:%(SENCHA)s/appbuilder/:%(SENCHA)s/jsbuilder:%(SENCHA)s/command:%(SENCHA)s" sencha build -p app.jsb3 -d .' % {'SENCHA': SENCHA})
  put('./core/static/app-all.js', '%(home)s/git/%(repo)s/core/static/app-all.js' % env)
  put('production_settings.py', '%(home)s/git/%(repo)s/local_settings.py' % env)
  put('production_db.yaml', '%(home)s/git/%(repo)s/gullwing/R/db.yaml' % env)
  run('cd %(home)s/git/%(repo)s/; git pull %(parent)s %(branch)s;'
      'sudo rm -rf %(www)s;'
      'sudo cp -R %(home)s/git/%(repo)s/ %(www)s;'
      'cd %(www)s;'
      'sudo rm -rf .git;'
      'sudo chown -R nginx:nginx %(www)s;'
      'python manage.py syncdb;'
      'sudo /etc/init.d/uwsgi.semurg reload' % env)
  run('sudo /etc/init.d/celeryd restart')
  local('cd core/static;rm app-all.js all-classes.js app.jsb3')


def reload():
  run('/etc/init.d/nginx reload;'
      '/etc/init.d/uwsgi.semurg reload')
