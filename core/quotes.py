# -*- coding: utf-8 -*-
from core.models import Currency
from core.models import Instrument
from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from logging import getLogger
from settings import EXCHANGE_MAP
from settings import INSTRUMENT_CURRENCY
from settings import PRICE_URL
from urllib2 import urlopen
from urllib2 import URLError

logger = getLogger('core.quotes')


def fetch_prices(symbol):
  pricehandler = urlopen(PRICE_URL % (symbol))
  data = pricehandler.read().rstrip().split(',')
  pricehandler.close()
  return {
    'close_price': Decimal(data[0]),
    'open_price': Decimal(data[1].replace('N/A', '0')),
    'last_price': Decimal(data[2]),
    'exchange': EXCHANGE_MAP[data[3].replace('"', '')]}


def update_instrument(symbol):
  try:
    instrument = Instrument.objects.get(symbol=symbol)
  except ObjectDoesNotExist:
    logger.info('Instrument %s did not exist, created', symbol)
    instrument = Instrument(symbol=symbol)
    instrument.currency = Currency.objects.get(symbol=INSTRUMENT_CURRENCY)

  symbol_data = fetch_prices(symbol)
  instrument.close_price = symbol_data['close_price']
  instrument.open_price = symbol_data['open_price']
  instrument.last_price = symbol_data['last_price']
  instrument.exchange = symbol_data['exchange']
  instrument.save()

  logger.info('Updated prices for %s: %.2f %.2f %.2f', 
      symbol,
      symbol_data['close_price'],
      symbol_data['open_price'],
      symbol_data['last_price'])

  return instrument


def update_prices():
  cursor = connection.cursor()
  cursor.execute('SELECT DISTINCT(symbol) FROM '
      '`core_position`, `core_instrument` WHERE '
      'core_position.instrument_id = core_instrument.id UNION '
      'SELECT DISTINCT(symbol) FROM core_opportunity')

  for row in cursor.fetchall():
    symbol = row[0]
    try:
      update_instrument(symbol)
    except Exception, e:
      logger.exception('Failed to get prices for %s', symbol)
