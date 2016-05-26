# -*- coding: utf-8 -*-
from django.forms import Form
from django.forms import ValidationError
from django.forms.util import ErrorList


class SemurgForm(Form):
  def add_error(self, field, message):
    if field not in self._errors:
      self._errors[field] = ErrorList()
    self._errors[field].append(message)

  def get_errors(self):
    return [{'id': field, 'msg': error.as_text()} for field, error in self.errors.items()]

  def clean(self):
    if self.errors:
      raise ValidationError('Basic validation has failed')
    return self.cleaned_data
