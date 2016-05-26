# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from celery.decorators import periodic_task
from celery.task.control import time_limit
from celery.task.schedules import crontab
from core.notification import notify_new_breakouts
from core.notification import notify_new_buys
from core.notification import notify_new_sells
from gullwing import run_engine
from gullwing.analytics import sync_orders
from gullwing.analytics import sync_watchlist
from gullwing.analytics import update_performance
from gullwing.quotes import update_prices
from gullwing.seller import find_sell_opportunities
from gullwing.screener import screen_stocks
from gullwing.sink import sync_breakouts
from gullwing.sink import sync_buy_opportunities
from logging import getLogger
from os import putenv
from time import time
from settings import DAYS_TO_FETCH
from settings import GULLWING_DB
from settings import QUOTES_URL
from settings import RUN_HOUR
from settings import RUN_MINUTES
from settings import SCREENER_URL

logger = getLogger('gullwing.tasks')


@periodic_task(run_every=crontab(hour=RUN_HOUR, minute=RUN_MINUTES, day_of_week=[1, 2, 3, 4, 5]))
def run_pipeline():
  logger.info('Running pipeline step 1 - screening stocks')
  t0 = time()
  screen_stocks(getLogger('gullwing.screener'), GULLWING_DB, SCREENER_URL)
  logger.info('Finished step 1 in %.2fs' % (time() - t0))

  t0 = time()
  logger.info('Running pipeline step 2 - updating prices')
  update_prices(
      getLogger('gullwing.quotes'),
      GULLWING_DB,
      QUOTES_URL,
      DAYS_TO_FETCH)
  logger.info('Finished step 2 in %.2fs' % (time() - t0))

  t0 = time()
  logger.info('Running pipeline step 3 - calculating breakpoints')
  run_engine()
  logger.info('Finished step 3 in %.2fs' % (time() - t0))

  t0 = time()
  logger.info('Running pipeline step 4 - copying results and generating charts')
  opportunities = sync_buy_opportunities()
  logger.info('Finished step 4 in %.2fs' % (time() - t0))

  t0 = time()
  logger.info('Running pipeline step 5 - copying breakout results')
  breakouts = sync_breakouts()
  logger.info('Finished step 5 in %.2fs' % (time() - t0))

  if opportunities:
    t0 = time()
    logger.info('Running pipeline step 6 - sending notifications')
    notify_new_buys(opportunities)
    logger.info('Finished step 6 in %.2fs' % (time() - t0))

  if breakouts:
    t0 = time()
    logger.info('Running pipeline step 7 - sending notifications')
    notify_new_breakouts(breakouts)
    logger.info('Finished step 7 in %.2fs' % (time() - t0))


@periodic_task(run_every=timedelta(seconds=30))
def run_seller():
  opportunities = find_sell_opportunities()
  if opportunities:
    notify_new_sells(opportunities)


@periodic_task(run_every=timedelta(minutes=10))
def run_performance():
  update_performance()


@periodic_task(run_every=timedelta(minutes=10))
def run_analytics():
  sync_orders()


@periodic_task(run_every=timedelta(minutes=10))
def sync_watches():
  sync_watchlist()


time_limit('gullwing.tasks.run_pipeline', soft=1200, hard=2400)
