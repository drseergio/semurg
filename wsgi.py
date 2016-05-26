# coding: utf-8
from django.core.handlers.wsgi import WSGIHandler
from os import environ
from os.path import dirname
from os.path import realpath
from sys import path

path.append(realpath(dirname(__file__)))

environ["CELERY_LOADER"] = "django"
environ['DJANGO_SETTINGS_MODULE'] = 'settings'

application = WSGIHandler()
