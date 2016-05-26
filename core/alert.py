# -*- coding: utf-8 -*-
from core.notification import send_alert_email
from core.models import Alert
from logging import getLogger

logger = getLogger('core.alert')


def check_alerts():
  alerts = Alert.objects.filter(target_reached=False)

  for alert in alerts:
    symbol = alert.instrument.symbol
    price = alert.target
    curr_price = alert.instrument.last_price

    if alert.alert_type == Alert.TYPE_SMALLER and curr_price < price:
      logger.info('Smaller than alert triggered for %s' % symbol)
      send_alert_email(alert)
      alert.target_reached = True
      alert.save()
    elif alert.alert_type == Alert.TYPE_GREATER and curr_price > price:
      logger.info('Greater than alert triggered for %s' % symbol)
      send_alert_email(alert)
      alert.target_reached = True
      alert.save()
