# -*- coding: utf-8 -*-
from datetime import timedelta
from celery.decorators import periodic_task
from core.alert import check_alerts
from core.quotes import update_prices
from settings import UPDATE_TIMEOUT


@periodic_task(run_every=timedelta(seconds=UPDATE_TIMEOUT))
def refresh_prices():
  update_prices()
  check_alerts()
