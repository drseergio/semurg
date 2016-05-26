# -*- coding: utf-8 -*-
from api import load_params
from core.forms.watched import WatchAddForm
from core.models import Watched
from django.db import transaction
from logging import getLogger
from piston.handler import BaseHandler
from piston.utils import rc

logger = getLogger('api.watched')


class WatchedHandler(BaseHandler):
  model = Watched

  def read(self, request):
    watched = Watched.objects.all().order_by('create_date')
    return self._handle_watched(watched)

  @transaction.commit_on_success
  def create(self, request, *args, **kwargs):
    params = load_params(request)
    form = WatchAddForm(params)

    if form.is_valid():
      watched = form.save()
      return {'success': True, 'id': watched.id}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def delete(self, request, watched_id):
    watched = Watched.objects.get(
        id=watched_id)
    watched.delete()
    return {'success': True}

  def _handle_watched(self, watched):
    watched_return = []
    for watch in watched:
      watched_return.append({
        'id': watch.id,
        'symbol': watch.instrument.symbol,
        'price': str(watch.instrument.last_price),
        'date': str(watch.create_date) })
    return {'items': watched_return}
