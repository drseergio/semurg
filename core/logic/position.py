# -*- coding: utf-8 -*-
from core.models import Order
from core.models import Position
from logging import getLogger

logger = getLogger('core.logic.position')


def get_total_equity():
  positions = Position.objects.filter(is_visible=True)
  total = 0
  for position in positions:
    total += position.instrument.last_price * position.quantity
  return total


def get_total_longterm():
  positions = Position.objects.filter(is_visible=True, is_longterm=True)
  total = 0
  for position in positions:
    total += position.instrument.last_price * position.quantity
  return total


def get_position_delta(position):
  order = Order.objects.get(position=position)
  original_amount = order.quantity * order.price
  current_amount = position.quantity * position.instrument.last_price
  delta = current_amount - original_amount
  pct = delta / original_amount
  return (delta, pct)
