# -*- coding: utf-8 -*-
from api import get_json_error_response
from piston.utils import rc
from settings import MAX_TRANSACTIONS_PER_PAGE


def require_args(arguments, method, rest=True):
  def inner(orig_func):
    def check(*args, **kwargs):
      if rest:
        request = args[1]
      else:
        request = args[0]

      if method == 'POST':
        arg_list = request.POST
      elif method == 'GET':
        arg_list = request.GET

      for argument in arguments:
        if not argument in arg_list:
          if rest:
            resp = rc.BAD_REQUEST
            resp.write("'%s' is a compulsory argument" % argument)
            return resp
          else:
            return get_json_error_response("'%s' is a compulsory argument" % argument)
      return orig_func(*args, **kwargs)
    return check
  return inner


def require_pager(orig_func):
  def check(*args, **kwargs):
    request = args[1]
    params = request.GET

    try:
      limit = int(params['limit'])
      if limit > MAX_TRANSACTIONS_PER_PAGE or limit < 0:
        resp = rc.BAD_REQUEST
        resp.write("'limit' is invalid")
        return resp
    except ValueError:
      resp = rc.BAD_REQUEST
      resp.write("'limit' must be an integer")
      return resp

    try:
      start = int(params['start'])
    except ValueError:
      resp = rc.BAD_REQUEST
      resp.write("'start' must be an integer")
      return resp

    return orig_func(*args, **kwargs)
  return check
