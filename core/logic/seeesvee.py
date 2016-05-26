# -*- coding: utf-8 -*-
from celery.task import task
from celery.registry import tasks
from core.logic import get_instrument
from core.logic.order import create_buy_order
from core.logic.order import create_sell_order
from core.models import Opportunity
from core.models import Position
from core.models import Transaction
from csv import reader
from decimal import Decimal
from django.core.cache import cache
from django.db import transaction as django_transaction
from logging import getLogger
from os import linesep

logger = getLogger('core.logic.seeesvee')


def get_export():
  transactions = Transaction.objects.all().order_by('date')

  entries = []
  for transaction in transactions:
    if transaction.transaction_type == Transaction.TYPE_DEPOSIT:
      entries.append({
          'date': str(transaction.date),
          'symbol': '',
          'type': 'deposit',
          'order_type': '',
          'price': '',
          'quantity': '',
          'fees': '',
          'total': transaction.amount,
          'description': transaction.description})
    elif transaction.transaction_type == Transaction.TYPE_WITHDRAWAL:
      entries.append({
          'date': str(transaction.date),
          'symbol': '',
          'type': 'withdrawal',
          'order_type': '',
          'price': '',
          'quantity': '',
          'fees': '',
          'total': transaction.amount,
          'description': transaction.description})
    elif transaction.order.order_type == Opportunity.TYPE_BUY:
      entries.append({
          'date': str(transaction.date),
          'symbol': transaction.order.instrument.symbol,
          'type': 'buy',
          'order_type': transaction.order.order_type,
          'price': transaction.order.price,
          'quantity': transaction.order.quantity,
          'fees': transaction.order.fees,
          'total': transaction.order.total,
          'description': transaction.description})
    else:
      entries.append({
          'date': str(transaction.date),
          'symbol': transaction.order.instrument.symbol,
          'type': 'sell',
          'order_type': transaction.order.order_type,
          'price': transaction.order.price,
          'quantity': transaction.order.quantity,
          'fees': transaction.order.fees,
          'total': transaction.order.total,
          'description': transaction.description})

  return entries


@task()
@django_transaction.commit_manually
def import_task(task_id=None):
  logger.info('Importing CSV data')
  import_data = cache.get('importdata')

  try:
    rows = reader(import_data.split(linesep)) 

    for row in rows:
      if len(row) != 10:
        continue

      if row[3] == 'deposit':
        _create_transaction(Transaction.TYPE_DEPOSIT, row[1], row[8], row[9])
      elif row[3] == 'withdrawal':
        _create_transaction(Transaction.TYPE_WITHDRAWAL, row[1], row[8], row[9])
      elif row[3] == 'buy':
        create_buy_order({
            'symbol': get_instrument(row[2]),
            'quantity': int(row[6]),
            'date': row[1],
            'price': Decimal(row[5]),
            'total': Decimal(row[8]),
            'fees': Decimal(row[7]) })
      elif row[3] == 'sell':
        instrument = get_instrument(row[2])
        position = Position.objects.filter(instrument=instrument, quantity=row[6])[0]
        create_sell_order({
            'position_id': position,
            'date': row[1],
            'price': Decimal(row[5]),
            'total': Decimal(row[8]),
            'fees': Decimal(row[7]) })
      else:
        continue

    django_transaction.commit()
  except Exception:
    django_transaction.rollback()
    logger.exception('Failed CSV import')

  cache.delete('importdata')


def _create_transaction(transaction_type, date, amount, description):
  transaction = Transaction()
  transaction.transaction_type = transaction_type
  transaction.date = date
  transaction.amount = Decimal(amount)
  transaction.description = description
  transaction.save()


tasks.register(import_task)
