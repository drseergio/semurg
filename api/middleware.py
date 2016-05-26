# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from piston.utils import rc


class NotFound(object):
  def process_exception(self, request, exception):
   if isinstance(exception, ObjectDoesNotExist):
     return rc.NOT_FOUND
   return None
