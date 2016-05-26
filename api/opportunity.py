# -*- coding: utf-8 -*-
from api import get_paged
from api import load_params
from api.decorators import require_args
from api.decorators import require_pager
from core.quotes import update_instrument
from core.logic import get_date_period
from core.logic import suggested_amount
from core.models import Instrument
from core.models import Opportunity
from datetime import date
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import simplejson
from logging import getLogger
from piston.handler import BaseHandler
from piston.utils import rc

logger = getLogger('api.opportunity')


class OpportunityHandler(BaseHandler):
  model = Opportunity

  @require_args(['limit', 'start'], 'GET')
  @require_pager
  def read(self, request):
    start = int(request.GET['start'])
    limit = int(request.GET['limit'])

    if 'filter' in request.GET:
      filtr = simplejson.loads(request.GET['filter'])
      value = filtr[0]['value']

      then = date.today() - timedelta(days=3)
      if int(value) == Opportunity.TYPE_BUY:
        opportunities = Opportunity.objects.filter(
            opportunity_type=value,
            date__gte=then,
            is_executed=0)
      else:
        opportunities = Opportunity.objects.filter(
            ~Q(opportunity_type=Opportunity.TYPE_BUY), date__gte=then, is_executed=0)
    else:
      opportunities = Opportunity.objects.all().order_by('-date')

    paged_opportunities = get_paged(opportunities, start, limit)
    return self._handle_opportunities(paged_opportunities, len(opportunities))

  def _handle_opportunities(self, opportunities, total):
    opportunities_return = []
    for opportunity in opportunities:
      try:
        instrument = Instrument.objects.get(symbol=opportunity.symbol)
      except ObjectDoesNotExist:
        logger.warn('Opportunity %s not shown, no data yet', opportunity.symbol)
        continue

      quantity, amount = suggested_amount(opportunity, instrument)
      if not opportunity.breakout_date:
        opportunity.breakout_date = 'N/A'

      opportunities_return.append({
        'id': opportunity.id,
        'symbol': opportunity.symbol,
        'quantity': quantity,
        'amount': amount,
        'breakout_date': str(opportunity.breakout_date),
        'date': str(opportunity.date),
        'price': str(instrument.last_price),
        'executed': int(opportunity.is_executed),
        'type': opportunity.opportunity_type,
        'period': get_date_period(opportunity.date) })
    return {'total': total, 'items': opportunities_return}
