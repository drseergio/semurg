# -*- coding: utf-8 -*-
from core.models import Breakout
from core.models import Instrument
from core.models import Opportunity
from core.models import Position
from django.core.exceptions import ObjectDoesNotExist
from gullwing import db_connect
from gullwing import generate_chart
from logging import getLogger
from MySQLdb import connect
from settings import GULLWING_DB

logger = getLogger('gullwing.sink')


def sync_buy_opportunities():
  conn, cursor = db_connect(GULLWING_DB)
  cursor.execute('SELECT * FROM buys')
  rows = cursor.fetchall()
  new_opportunities = []
  for row in rows:
    symbol = row[0]
    date = row[1]

    try:
      Opportunity.objects.get(
          opportunity_type=Opportunity.TYPE_BUY,
          date=date,
          symbol=symbol)
      # exclude opportunities for instruments we own already 
      instrument = Instrument.objects.get(symbol=symbol)
      if Position.objects.filter(instrument=instrument, is_visible=True):
        raise ObjectDoesNotExist
    except ObjectDoesNotExist:
      logger.info('Sinking buy opportunity for %s', symbol)
      opportunity = Opportunity(
          opportunity_type=Opportunity.TYPE_BUY,
          date=date,
          symbol=symbol,
          breakout_date=row[3])
      generate_chart(symbol, date)
      opportunity.save()
      new_opportunities.append(opportunity)

  cursor.close()
  conn.close()
  return new_opportunities


def sync_breakouts():
  conn, cursor = db_connect(GULLWING_DB)
  cursor.execute('SELECT * FROM breakouts')
  rows = cursor.fetchall()
  new_breakouts = []
  for row in rows:
    symbol = row[0]
    date = row[1]

    try:
      Breakout.objects.get(symbol=symbol, date=date)
    except ObjectDoesNotExist:
      logger.info('Sinking breakout %s', symbol)
      breakout = Breakout(symbol=symbol, date=date, price=row[2])
      breakout.save()
      new_breakouts.append(breakout)

  cursor.close()
  conn.close()
  return new_breakouts
