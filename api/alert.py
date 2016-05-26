# -*- coding: utf-8 -*-
from api import load_params
from core.forms.alert import AlertAddForm
from core.forms.alert import AlertEditForm
from core.models import Alert
from django.db import transaction
from logging import getLogger
from piston.handler import BaseHandler
from piston.utils import rc

logger = getLogger('api.alert')


class AlertHandler(BaseHandler):
  model = Alert

  def read(self, request):
    alerts = Alert.objects.all()
    return self._handle_alerts(alerts)

  @transaction.commit_on_success
  def create(self, request, *args, **kwargs):
    params = load_params(request)
    form = AlertAddForm(params)

    if form.is_valid():
      alert = form.save()
      return {'success': True, 'id': alert.id}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def delete(self, request, alert_id):
    alert = Alert.objects.get(
        id=alert_id)
    alert.delete()
    return {'success': True}

  @transaction.commit_on_success
  def update(self, request, alert_id):
    params = load_params(request)
    params['id'] = alert_id

    form = AlertEditForm(params)
    if form.is_valid():
      form.save()
      return {'success': True}
    else:
      return {'success': False, 'errors': form.get_errors()}

  def _handle_alerts(self, alerts):
    alerts_return = []
    for alert in alerts:
      alerts_return.append({
        'id': alert.id,
        'symbol': alert.instrument.symbol,
        'price': str(alert.instrument.last_price),
        'target': str(alert.target),
        'type': alert.alert_type,
        'target_reached': int(alert.target_reached) })
    return {'items': alerts_return}
