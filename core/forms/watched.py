# -*- coding: utf-8 -*-
from core.forms import SemurgForm
from core.logic import get_instrument
from core.models import Watched
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.forms import CharField
from django.forms import ValidationError
from logging import getLogger

logger = getLogger('core.forms.watched')


class WatchAddForm(SemurgForm):
  symbol = CharField()

  def clean_symbol(self):
    symbol = self.cleaned_data['symbol']
    try:
      instrument = get_instrument(symbol)
      try:
        Watched.objects.get(instrument=instrument)
        raise ValidationError('Watch already exists')
      except ObjectDoesNotExist:
        pass
    except:
      logger.exception('Failed to get instrument')
      raise ValidationError('Instrument does not exist and sync failed')
    return instrument

  def save(self):
    instrument = self.cleaned_data['symbol']
    watch = Watched(create_date=datetime.now(), instrument=instrument)
    watch.save()
    return watch
