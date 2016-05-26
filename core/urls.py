# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns


urlpatterns = patterns(
  'core.views',
  (r'^$', 'app.index'),
  (r'^performance$', 'app.performance'))
