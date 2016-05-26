# -*- coding: utf-8 -*-
from core.forms import SemurgForm
from django.forms import FileField
from django.forms import ValidationError
from logging import getLogger
from settings import MAX_IMPORT_SIZE

logger = getLogger('core.forms.seeesvee')


class ImportForm(SemurgForm):
  importdata = FileField()

  def clean_importdata(self):
    data = self.cleaned_data['importdata']
    if data.size > MAX_IMPORT_SIZE:
      raise ValidationError('Too much money. The limit is 100KB.')
    return data
