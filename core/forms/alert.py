# -*- coding: utf-8 -*-
from core.forms import SemurgForm
from core.logic import get_instrument
from core.models import Alert
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.forms import CharField
from django.forms import ChoiceField
from django.forms import DecimalField
from django.forms import ModelChoiceField
from django.forms import ValidationError
from logging import getLogger

logger = getLogger('core.forms.alert')


class AlertAddForm(SemurgForm):
  symbol = CharField()
  type = ChoiceField(choices=Alert.TYPES)
  target = DecimalField(initial=0.0)

  def clean_target(self):
    amount = self.cleaned_data['target']
    if amount and amount <= 0:
      raise ValidationError(
          'Target cannot be negative')
    return amount

  def clean_symbol(self):
    symbol = self.cleaned_data['symbol']
    try:
      instrument = get_instrument(symbol)
    except:
      raise ValidationError('Instrument does not exist and sync failed')
    return instrument

  def save(self):
    instrument = self.cleaned_data['symbol']
    alert = Alert(
        instrument=instrument,
        alert_type=self.cleaned_data['type'],
        target=self.cleaned_data['target'])
    alert.save()
    return alert


class AlertEditForm(SemurgForm):
  target = DecimalField(initial=0.0)

  def __init__(self, *args, **kwargs):
    super(AlertEditForm, self).__init__(*args, **kwargs)
    self.fields['id'] = ModelChoiceField(queryset=Alert.objects.all())

  def clean_target(self):
    amount = self.cleaned_data['target']
    if amount and amount <= 0:
      raise ValidationError(
          'Target cannot be negative')
    return amount

  def save(self):
    alert = self.cleaned_data['id']
    alert.target = self.cleaned_data['target']
    alert.save()
