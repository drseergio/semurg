# -*- coding: utf-8 -*-
from core.models import Currency
from core.models import Instrument
from core.models import Opportunity
from core.models import Order
from core.models import Position
from core.models import Transaction
from core.quotes import fetch_prices
from datetime import datetime
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from logging import getLogger
from pytz import timezone
from pytz import utc
from settings import INSTRUMENT_CURRENCY
from settings import ORDER_SIZE

logger = getLogger('core.logic')


def is_market_open():
  tz = timezone('US/Eastern')

  now = datetime.now(utc)
  now_ny = datetime.now(tz)

  if now_ny.isoweekday() == 7 or now_ny.isoweekday() == 6:
    return False 

  open_time = tz.localize(datetime(year=now.year, month=now.month, day=now.day, hour=9, minute=30))
  open_time_local = open_time.astimezone(utc)
  close_time = tz.localize(datetime(year=now.year, month=now.month, day=now.day, hour=16))
  close_time_local = close_time.astimezone(utc)

  if now > open_time_local and now < close_time_local:
    return True

  return False


def get_portfolio_delta():
  positions = Position.objects.filter(is_visible=True)
  present_value = 0
  original_value = 0

  for position in positions:
    present_value += position.quantity * position.instrument.last_price
    order = Order.objects.get(position=position)
    original_value += position.quantity * order.price

  if original_value == 0:
    return (0, 0)

  delta = present_value - original_value
  pct = round((delta / original_value) * 100, 2)
  return (delta, pct)


def get_winning_trades():
  return len(Order.objects.filter(
      ~Q(order_type=Opportunity.TYPE_BUY),
      Q(winning=True)))


def get_profit_reached():
  return len(Order.objects.filter(
      ~Q(order_type=Opportunity.TYPE_BUY),
      Q(profit_reached=True)))


def get_losing_trades():
  return len(Order.objects.filter(
      ~Q(order_type=Opportunity.TYPE_BUY),
      Q(winning=False)))


def suggested_amount(opportunity, instrument):
  quantity = int(ORDER_SIZE / instrument.last_price)
  amount = quantity * instrument.last_price
  return (quantity, amount)


def get_instrument(symbol):
  try:
    instrument = Instrument.objects.get(symbol=symbol)
  except ObjectDoesNotExist:
    price_data = fetch_prices(symbol)
    instrument = Instrument(
        symbol=symbol,
        currency=Currency.objects.get(symbol=INSTRUMENT_CURRENCY),
        close_price=price_data['close_price'],
        open_price=price_data['open_price'],
        last_price=price_data['last_price'],
        exchange=price_data['exchange'])
    instrument.save()
  return instrument


def get_date_period(date):
  period = 'Older'

  if is_future(date):
    period = 'Future'
  elif is_today(date):
    period = 'Today'
  elif is_yesterday(date):
    period = 'Yesterday'
  elif is_last_three_days(date):
    period = 'Last 3 days'
  elif is_later_than_this_monday(date):
    period = 'This week'
  elif is_later_than_last_monday(date):
    period = 'Last week'
  elif is_later_than_first_of_this_month(date):
    period = 'This month'
  elif is_later_than_first_of_last_month(date):
    period = 'Last month'
  elif is_later_than_first_of_this_year(date):
    period = 'This fiscal year'

  return period


def is_future(date):
  today = datetime.today().date()
  delta = (today - date).days

  if delta < 0:
    return True
  return False


def is_today(date):
  today = datetime.today().date()
  delta = (today - date).days

  if delta == 0:
    return True
  return False


def is_yesterday(date):
  today = datetime.today().date()
  delta = (today - date).days

  if delta == 1:
    return True
  return False


def is_last_three_days(date):
  today = datetime.today().date()
  delta = (today - date).days

  if delta > 1 and delta <= 3:
    return True
  return False


def is_later_than_this_monday(date):
  monday_spec = datetime.today().strftime('%Y %W 1')
  monday_date = datetime.strptime(monday_spec, '%Y %W %w').date()
  delta = (date - monday_date).days

  if delta >= 0:
    return True
  return False


def is_later_than_last_monday(date):
  lastweek_date = datetime.today() + timedelta(weeks=-1)
  monday_spec = lastweek_date.strftime('%Y %W 1')
  monday_date = datetime.strptime(monday_spec, '%Y %W %w').date()
  delta = (date - monday_date).days

  if delta >= 0:
    return True
  return False


def is_later_than_first_of_this_month(date):
  first_spec = datetime.today().strftime('%Y %m 1')
  first_date = datetime.strptime(first_spec, '%Y %m %d').date()
  delta = (date - first_date).days

  if delta >= 0:
    return True
  return False


def is_later_than_first_of_last_month(date):
  thismonth_spec = datetime.today().strftime('%Y %m 1')
  thismonth_date = datetime.strptime(thismonth_spec, '%Y %m %d').date()
  lastmonth_date = thismonth_date + timedelta(days=-1)
  first_spec = lastmonth_date.strftime('%Y %m 1')
  first_date = datetime.strptime(first_spec, '%Y %m %d').date()
  delta = (date - first_date).days

  if delta >= 0:
    return True
  return False


def is_later_than_first_of_this_year(date):
  first_spec = datetime.today().strftime('%Y 1 1')
  first_date = datetime.strptime(first_spec, '%Y %m %d').date()
  delta = (date - first_date).days

  if delta >= 0:
    return True
  return False
