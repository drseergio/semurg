# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from gullwing.analytics import update_performance
from logging import getLogger
from settings import ACCOUNT_CURRENCY
from settings import ANALYTICS_PORTFOLIO_ID
from settings import DEBUG

logger = getLogger('core.view')


def index(request):
  return render_to_response(
      'app.html', {
          'currency': ACCOUNT_CURRENCY,
          'debug': DEBUG },
      context_instance=RequestContext(request))


def performance(request):
  performance = cache.get('performance')
  if not performance:
    logger.info('Performance data not in cache, requesting update')
    performance = update_performance()
  return render_to_response(
      'performance.html', {
          'debug': DEBUG,
          'portfolio_id': ANALYTICS_PORTFOLIO_ID, 
          'performance': performance },
      context_instance=RequestContext(request))
