# -*- coding: utf-8 -*-
from api import get_paged
from api import load_params
from api.decorators import require_args
from api.decorators import require_pager
from core.forms.breakout import BreakoutEditForm
from core.models import Breakout
from datetime import date
from django.db import transaction
from logging import getLogger
from piston.handler import BaseHandler
from piston.utils import rc

logger = getLogger('api.breakout')


class BreakoutHandler(BaseHandler):
  model = Breakout

  @require_args(['limit', 'start'], 'GET')
  @require_pager
  def read(self, request):
    start = int(request.GET['start'])
    limit = int(request.GET['limit'])

    breakouts = Breakout.objects.all().order_by('-date')
    paged_breakouts = get_paged(breakouts, start, limit)
    return self._handle_breakouts(paged_breakouts, len(breakouts))

  @transaction.commit_on_success
  def update(self, request, breakout_id):
    params = load_params(request)
    params['id'] = breakout_id

    form = BreakoutEditForm(params)
    if form.is_valid():
      form.save()
      return {'success': True}
    else:
      return {'success': False, 'errors': form.get_errors()}

  def _handle_breakouts(self, breakouts, total):
    breakouts_return = []
    for breakout in breakouts:
      breakouts_return.append({
        'id': breakout.id,
        'symbol': breakout.symbol,
        'date': str(breakout.date),
        'reviewed': int(breakout.reviewed),
        'price': str(breakout.price) })
    return {'total': total, 'items': breakouts_return}
