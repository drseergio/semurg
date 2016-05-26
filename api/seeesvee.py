# -*- coding: utf-8 -*-
from api import JSON_FAILURE_EMPTY
from api import JSON_SUCCESS
from api import get_json_errors
from api import get_json_error_response
from core.forms.seeesvee import ImportForm
from core.logic.seeesvee import import_task
from core.logic.seeesvee import get_export
from csv import writer
from datetime import datetime
from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from logging import getLogger

logger = getLogger('api.csv')


def export(request):
  entries = get_export()

  response = HttpResponse(mimetype='text/csv')
  response['Content-Disposition'] = ('attachment; filename=semurg-'
      '%s.csv') % (
          datetime.now().strftime('%Y%m%d'))
  csv_writer = writer(response)

  i = 0
  for entry in entries:
    csv_writer.writerow([
        i,
        entry['date'],
        entry['symbol'],
        entry['type'],
        entry['order_type'],
        entry['price'],
        entry['quantity'],
        entry['fees'],
        entry['total']])
    i += 1

  return response


@csrf_exempt
def upload(request):
  form = ImportForm(
      request.POST,
      request.FILES)
  if form.is_valid():
    try:
      cache.set('importdata', request.FILES['importdata'].read()) 
      import_task.apply_async(task_id='import')
      return HttpResponse(JSON_SUCCESS)
    except Exception, e:
      logger.info(e)
      return get_json_error_response(e)
  else:
    return get_json_errors(form.errors)


def progress(request):
  if cache.get('importdata'):
    return HttpResponse(JSON_FAILURE_EMPTY)
  else:
    return HttpResponse(JSON_SUCCESS)
