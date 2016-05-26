# -*- coding: utf-8 -*-
from core.models import Opportunity
from core.models import Order
from core.models import Position
from core.models import Transaction
from logging import getLogger

logger = getLogger('core.logic.order')


def create_buy_order(order_data):
  instrument = order_data['symbol']
  position = Position(
      instrument=instrument,
      quantity=order_data['quantity'],
      date=order_data['date'],
      buy_price=order_data['price'])
  position.save()

  if 'opportunity' in order_data and order_data['opportunity'] != None:
    opportunity = order_data['opportunity']
    opportunity.is_executed = True
    opportunity.save()
  else:
    opportunity = None

  order = Order(
      order_type=Opportunity.TYPE_BUY,
      instrument=instrument,
      quantity=order_data['quantity'],
      date=order_data['date'],
      price=order_data['price'],
      fees=order_data['fees'],
      opportunity=opportunity,
      total=order_data['total'],
      position=position)
  order.save()

  transaction = Transaction(
      amount=order_data['total'],
      date=order_data['date'],
      description='Buy %d %s @ %.2f' % (
          order_data['quantity'], instrument.symbol, order_data['price']),
      order=order,
      transaction_type=Transaction.TYPE_BUY)
  transaction.save()
  return order


def create_sell_order(order_data):
  position = order_data['position_id']
  position.is_visible = False
  position.save()

  if 'opportunity' in order_data and order_data['opportunity'] != None:
    opportunity = order_data['opportunity']
    opportunity.is_executed = True
    opportunity.save()
  else:
    opportunity = None

  if position.is_profit():
    order_type = Opportunity.TYPE_SELL
  else:
    order_type = Opportunity.TYPE_SELL_T

  buy_order = Order.objects.get(position=position, order_type=Opportunity.TYPE_BUY)

  order = Order(
      order_type=order_type,
      instrument=position.instrument,
      quantity=position.quantity,
      date=order_data['date'],
      price=order_data['price'],
      opportunity=opportunity,
      fees=order_data['fees'],
      total=order_data['total'],
      related_order=buy_order,
      position=position)
  order.save()

  transaction = Transaction(
      amount=order_data['total'],
      date=order_data['date'],
      description='Sell %d %s @ %.2f' % (
          position.quantity, position.instrument.symbol, order_data['price']),
      order=order,
      transaction_type=Transaction.TYPE_SELL)
  transaction.save()
  return order
