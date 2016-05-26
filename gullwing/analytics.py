# -*- coding: utf-8 -*-
from core.logic import get_losing_trades
from core.logic import get_profit_reached
from core.logic import get_winning_trades
from core.logic.position import get_total_equity
from core.logic.position import get_total_longterm
from core.models import Instrument
from core.models import Opportunity
from core.models import Order
from core.models import Position
from core.models import Transaction
from core.models import Watched
from datetime import date
from datetime import datetime
from datetime import time
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from gdata.finance import Commission
from gdata.finance import Money
from gdata.finance import Price
from gdata.finance import TransactionData
from gdata.finance import TransactionEntry
from gdata.finance.service import FinanceService
from gdata.finance.service import PortfolioQuery
from gdata.finance.service import PositionQuery
from logging import getLogger
from re import compile
from settings import ANALYTICS_PASSWORD
from settings import ANALYTICS_USERNAME
from settings import ANALYTICS_SERVICE
from settings import ANALYTICS_PORTFOLIO_ID
from settings import ANALYTICS_WATCHLIST_ID
from settings import INSTRUMENT_CURRENCY

logger = getLogger('gullwing.analytics')


_TYPES = {
    Opportunity.TYPE_BUY: 'Buy',
    Opportunity.TYPE_SELL: 'Sell',
    Opportunity.TYPE_SELL_T: 'Sell' }
GDATA_SYMBOL_REGEXP = compile(r'\w+:(\w+)')


def sync_orders():
  client = _get_client()
  orders = Order.objects.filter(reconciled=True, synchronized=False)
  for order in orders:
    _sync_order(client, order)
  if orders:
    logger.info('Successfully synced %d orders', len(orders))


def update_performance():
  client = _get_client()
  query = PortfolioQuery()
  query.returns = True
  query.transactions = False
  portfolio = client.GetPortfolio(
      portfolio_id=ANALYTICS_PORTFOLIO_ID,
      query=query).portfolio_data

  losing_trades = get_losing_trades()
  winning_trades = get_winning_trades()
  profit_reached = get_profit_reached()
  total_trades = losing_trades + winning_trades

  total_amount = get_total_equity()
  longterm_amount = get_total_longterm()
  longterm_pct = 0
  shortterm_amount = total_amount - longterm_amount
  shortterm_pct = 0

  if total_amount:
    longterm_pct = round((longterm_amount / total_amount) * 100, 2)
    shortterm_pct = round((shortterm_amount / total_amount) * 100, 2)

  performance = {
    'last_update': datetime.now(),
    '1w': round(float(portfolio.return1w) * 100, 2),
    '4w': round(float(portfolio.return4w) * 100, 2),
    '3m': round(float(portfolio.return3m) * 100, 2),
    'YTD': round(float(portfolio.returnYTD) * 100, 2),
    '1y': round(float(portfolio.return1y) * 100, 2),
    '3y': round(float(portfolio.return3y) * 100, 2),
    '5y': round(float(portfolio.return5y) * 100, 2),
    'overall':round(float(portfolio.return_overall) * 100, 2),
    'total_trades': total_trades,
    'losing_trades': losing_trades,
    'profit_reached': profit_reached,
    'winning_trades': winning_trades,
    'longterm_pct': longterm_pct,
    'shortterm_pct': shortterm_pct }

  cache.set('performance', performance)
  return performance


def sync_watchlist():
  client = _get_client()

  query = PositionQuery()
  positions = client.GetPositionFeed(
      portfolio_id=ANALYTICS_WATCHLIST_ID, query=query).entry
  remote_symbols = [
      GDATA_SYMBOL_REGEXP.match(position.ticker_id).groups()[0] for position in positions]

  local_watches = Watched.objects.filter(synchronized=False)

  for watch in local_watches:
    logger.info('Sinking watch (semurg>finance) for %s', watch.instrument.symbol)
    ticker = '%s:%s' % (watch.instrument.exchange, watch.instrument.symbol)
    txn = TransactionEntry(transaction_data=TransactionData(
        type='Buy',
        notes=None))

    logger.info(client.AddTransaction(
        txn,
        portfolio_id=ANALYTICS_WATCHLIST_ID,
        ticker_id=ticker))
   
    watch.synchronized = True
    watch.save()

  for remote_symbol in remote_symbols:
    try:
      instrument = Instrument.objects.get(symbol=remote_symbol)
      try:
        Watched.objects.get(instrument=instrument)  # check if watch exists
      except ObjectDoesNotExist:
        logger.info('Sinking watch (finance>semurg) for %s', remote_symbol)
        watch = Watched(
            instrument=instrument,
            create_date=date.today(),
            synchronized=True)
        watch.save()
    except ObjectDoesNotExist:
      pass  # we don't have such instrument available


def _sync_order(client, order):
  logger.info(
      'Synchronizing %s order for %s with Google',
      _TYPES[order.order_type],
      order.instrument.symbol)

  ticker = '%s:%s' % (order.instrument.exchange, order.instrument.symbol)
  txn_type = _TYPES[order.order_type]
  date = datetime.combine(order.date, time())
  shares = str(order.quantity)
  price = Price(money=[Money(amount=str(order.price), currency_code=INSTRUMENT_CURRENCY)])
  commission = Commission(money=[Money(amount=str(order.fees), currency_code=INSTRUMENT_CURRENCY)])

  txn = TransactionEntry(transaction_data=TransactionData(
      type=txn_type,
      date=date.isoformat(),
      shares=shares,
      commission=commission,
      notes=None,
      price=price))

  logger.info(client.AddTransaction(
      txn,
      portfolio_id=ANALYTICS_PORTFOLIO_ID,
      ticker_id=ticker))

  order.synchronized = True
  order.save()


def _get_client():
  client = FinanceService()
  client.ClientLogin(
      ANALYTICS_USERNAME,
      ANALYTICS_PASSWORD, service=ANALYTICS_SERVICE)
  return client
