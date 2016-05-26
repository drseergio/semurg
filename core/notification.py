# -*- coding: utf-8 -*-
from core.models import Instrument
from core.models import Opportunity
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from logging import getLogger
from os.path import join
from settings import ANALYTICS_PORTFOLIO_ID
from settings import CHARTS_PATH
from settings import RECIPIENT_EMAIL
from settings import SENDER_EMAIL
from settings import SEMURG_HOST

logger = getLogger('core.notification')


def notify_new_sells(opportunities):
  send_opportunity_email('SEMURG: New sell opportunities identified', 'email_sell', opportunities)


def notify_new_buys(opportunities):
  send_opportunity_email('SEMURG: New buy opportunities identified', 'email_buy', opportunities)


def notify_new_breakouts(breakouts):
  t_plain = get_template('email_breakout.txt')
  t_html = get_template('email_breakout.html')
  c = Context({
      'semurg_host': SEMURG_HOST,
      'portfolio_id': ANALYTICS_PORTFOLIO_ID,
      'breakouts': breakouts })
  msg = EmailMultiAlternatives(
      'SEMURG: New breakouts found',
      t_plain.render(c),
      SENDER_EMAIL,
      [RECIPIENT_EMAIL])
  msg.attach_alternative(t_html.render(c), 'text/html')
  msg.send()


def send_opportunity_email(subject, template, opportunities):
  for opportunity in opportunities:
    try:
      opportunity.instrument = Instrument.objects.get(symbol=opportunity.symbol)
    except ObjectDoesNotExist:
      pass
    opportunity.type = Opportunity.TYPES[opportunity.opportunity_type-1][1]
  logger.info('Sending notification e-mail to %s', RECIPIENT_EMAIL)
  t_plain = get_template('%s.txt' % template)
  t_html = get_template('%s.html' % template)
  c = Context({
      'semurg_host': SEMURG_HOST,
      'portfolio_id': ANALYTICS_PORTFOLIO_ID,
      'opportunities': opportunities })
  msg = EmailMultiAlternatives(subject, t_plain.render(c), SENDER_EMAIL, [RECIPIENT_EMAIL])
  msg.attach_alternative(t_html.render(c), 'text/html')

  for opportunity in opportunities:
    try:
      opportunity_date = opportunity.date.strftime('%Y-%m-%d')
      symbol = opportunity.symbol
      chart_filename = join(CHARTS_PATH, symbol, '%s.png' % opportunity_date)
      chart_data = open(chart_filename, 'r').read()
      msg.attach('%s-%s.png' % (symbol, opportunity_date), chart_data, 'image/png')
    except Exception:
      logger.exception('Failed to attach chart for %s' % opportunity.symbol)

  msg.send()


def send_alert_email(alert):
  t_plain = get_template('email_alert.txt')
  t_html = get_template('email_alert.html')
  c = Context({
      'semurg_host': SEMURG_HOST,
      'portfolio_id': ANALYTICS_PORTFOLIO_ID,
      'symbol': alert.instrument.symbol,
      'price': alert.instrument.last_price })
  msg = EmailMultiAlternatives(
      'SEMURG: Price alert for %s' % alert.instrument.symbol,
      t_plain.render(c),
      SENDER_EMAIL,
      [RECIPIENT_EMAIL])
  msg.attach_alternative(t_html.render(c), 'text/html')
  msg.send()
