# coding: utf-8
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    (r'^api/', include('api.urls')),
    (r'^', include('core.urls')))

urlpatterns += patterns('',
    (r'^logs/', include('sentry.web.urls')))

urlpatterns += staticfiles_urlpatterns()
