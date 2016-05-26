# -*- coding: utf-8 -*-
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import simplejson


JSON_SUCCESS = '{"success":true}'
JSON_FAILURE = '{"success":false,"message":"%s"}'
JSON_FAILURE_EMPTY = '{"success":false}'


def get_json_response(objects, handler=None, total=None):
  objects_envelope = []

  if handler:
    for obj in objects:
      objects_envelope.append(handler(obj))
  else:
    objects_envelope = objects

  if total:
    return_dict = {'count': total, 'items': objects_envelope}
  else:
    return_dict = {'count': len(objects_envelope), 'items': objects_envelope}

  return HttpResponse(simplejson.dumps(return_dict))


def get_paged(objects, start, limit):
  page = start / limit + 1
  paginator = Paginator(objects, limit)
  try:
    paged_objects = paginator.page(page).object_list
  except EmptyPage:
    paged_objects = paginator.page(paginator.num_pages).object_list
  return paged_objects


def load_params(request):
  try:
    return simplejson.loads(request.raw_post_data)
  except Exception:
    raise ValueError('invalid arguments')


def get_json_response_object(obj, handler):
  return HttpResponse(simplejson.dumps([handler(obj)]))


def form_handler(error):
  return error.as_text()


def str_handler(error):
  return error


def get_json_errors(errors, handler=form_handler):
  response = '{"success":false, "errors":['
  response += ','.join(['{"id":"%s","msg":"%s"}' % (field, handler(error))
    for field, error in errors.items()])
  response += ']}'
  return HttpResponse(status=200, content=response)


def get_json_error_response(message="", code=400):
  if message:
    content = JSON_FAILURE % message
  else:
    content = JSON_FAILURE_EMPTY
  return HttpResponse(status=code, content=content)
