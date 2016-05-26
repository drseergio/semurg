# -*- coding: utf-8 -*-
from core.models import Opportunity
from core.models import Order
from core.models import Position
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from gullwing import generate_chart
from logging import getLogger
from settings import MAX_HOLD_DAYS
from settings import PROFIT_TARGET

logger = getLogger('gullwing.seller')


def find_sell_opportunities():
  positions = Position.objects.filter(is_visible=True, is_longterm=False)
  opportunities = []
  for position in positions:
    today = date.today()
    days = (today - position.date).days

    position_value = position.quantity * position.instrument.last_price
    order = Order.objects.get(position=position)
    original_value = order.quantity * order.price
    value_change = (position_value - original_value) / original_value

    if value_change >= PROFIT_TARGET or days >= MAX_HOLD_DAYS:
      try:
        Opportunity.objects.get(
            Q(symbol=position.instrument.symbol),
            Q(opportunity_type=Opportunity.TYPE_SELL_T) | \
            Q(opportunity_type=Opportunity.TYPE_SELL))
      except ObjectDoesNotExist:
        if days >= MAX_HOLD_DAYS:
          logger.info('Found sell opportunity for %s based on holding period',
              position.instrument.symbol)
          opportunity = Opportunity(
              symbol=position.instrument.symbol,
              date=today,
              opportunity_type=Opportunity.TYPE_SELL_T)
        elif value_change >= PROFIT_TARGET:
          logger.info('Found sell opportunity for %s based on profit',
              position.instrument.symbol)
          opportunity = Opportunity(
              symbol=position.instrument.symbol,
              date=today,
              opportunity_type=Opportunity.TYPE_SELL)
        opportunity.save()
        opportunities.append(opportunity)
        generate_chart(position.instrument.symbol, today)
  return opportunities
