# -*- coding: utf-8 -*-
from api import load_params
from core.forms.position import PositionEditForm
from core.logic.position import get_position_delta
from core.models import Position
from datetime import date
from logging import getLogger
from piston.handler import BaseHandler
from piston.utils import rc


logger = getLogger('api.position')


class PositionHandler(BaseHandler):
  model = Position

  def read(self, request, position_id=None):
    positions = Position.objects.filter(is_visible=True)
    return self._handle_positions(positions)

  def update(self, request, position_id):
    params = load_params(request)
    params['id'] = position_id

    form = PositionEditForm(params)
    if form.is_valid():
      form.save()
      return {'success': True}
    else:
      return {'success': False, 'errors': form.get_errors()}

  def _handle_positions(self, positions):
    positions_return = []
    for position in positions:
      delta, pct = get_position_delta(position)
      positions_return.append({
        'id': position.id,
        'symbol': position.instrument.symbol,
        'quantity': position.quantity,
        'orig': position.buy_price,
        'days': (date.today()-position.date).days,
        'price': position.instrument.last_price,
        'close': position.instrument.close_price,
        'longterm': int(position.is_longterm),
        'open': position.instrument.open_price,
        'value': str(position.quantity * position.instrument.last_price),
        'date': str(position.date),
        'delta_pct': str(pct),
        'delta': str(delta)})
    return {'items': positions_return}
