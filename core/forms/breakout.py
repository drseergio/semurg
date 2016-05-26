# -*- coding: utf-8 -*-
from core.forms import SemurgForm
from core.models import Breakout
from django.forms import BooleanField
from django.forms import ModelChoiceField
from logging import getLogger

logger = getLogger('core.forms.order')


class BreakoutEditForm(SemurgForm):
  reviewed = BooleanField(required=False)

  def __init__(self, *args, **kwargs):
    super(BreakoutEditForm, self).__init__(*args, **kwargs)
    self.fields['id'] = ModelChoiceField(queryset=Breakout.objects.all())

  def save(self):
    breakout = self.cleaned_data['id']
    breakout.reviewed = self.cleaned_data['reviewed']
    breakout.save()
