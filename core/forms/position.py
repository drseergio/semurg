# -*- coding: utf-8 -*-
from core.forms import SemurgForm
from core.models import Position
from django.forms import BooleanField
from django.forms import IntegerField
from django.forms import ModelChoiceField
from logging import getLogger

logger = getLogger('core.forms.position')


class PositionEditForm(SemurgForm):
  longterm = BooleanField(required=False)
  quantity = IntegerField(min_value=1)

  def __init__(self, *args, **kwargs):
    super(PositionEditForm, self).__init__(*args, **kwargs)
    self.fields['id'] = ModelChoiceField(queryset=Position.objects.all())

  def save(self):
    position = self.cleaned_data['id']
    position.is_longterm = self.cleaned_data['longterm']
    position.quantity = self.cleaned_data['quantity']
    position.save()
