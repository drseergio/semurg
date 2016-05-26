# -*- coding: utf-8 -*-
from api import get_paged
from api import load_params
from api.decorators import require_args
from api.decorators import require_pager
from core.models import Opportunity
from core.models import Order
from core.models import Transaction
from core.forms.order import OrderBuyForm
from core.forms.order import OrderEditForm
from core.forms.order import OrderSellForm
from django.db import transaction
from logging import getLogger
from piston.handler import BaseHandler
from piston.utils import rc

logger = getLogger('api.order')


class OrderHandler(BaseHandler):
  model = Order

  @require_args(['limit', 'start'], 'GET')
  @require_pager
  def read(self, request, transaction_id=None):
    start = int(request.GET['start'])
    limit = int(request.GET['limit'])

    orders = Order.objects.all().order_by('-date')
    paged_orders = get_paged(orders, start, limit)

    return self._handle_orders(paged_orders, len(orders))

  @transaction.commit_on_success
  def create(self, request, *args, **kwargs):
    params = load_params(request)

    if 'opportunity' in params and int(params['opportunity']) == 0:
      del params['opportunity']

    try:
      if 'type' in params and int(params['type']) == Opportunity.TYPE_SELL:
        form = OrderSellForm(params)
      else:
        form = OrderBuyForm(params)
    except ValueError:
      return rc.BAD_REQUEST

    if form.is_valid():
      order = form.save()
      return {'success': True, 'id': order.id}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def delete(self, request, order_id):
    order = Order.objects.get(
        id=order_id)
    if order.reconciled:
      return {'success': False}
    else:
      transaction = Transaction.objects.get(order=order)
      transaction.delete()
      return {'success': True}

  @transaction.commit_on_success
  def update(self, request, order_id):
    params = load_params(request)
    params['id'] = order_id

    form = OrderEditForm(params)
    if form.is_valid():
      form.save()
      return {'success': True}
    else:
      return {'success': False, 'errors': form.get_errors()}

  def _handle_orders(self, orders, total):
    orders_return = []
    for order in orders:
      orders_return.append({
        'id': order.id,
        'symbol': order.instrument.symbol,
        'date': str(order.date),
        'type': order.order_type,
        'quantity': order.quantity,
        'price': str(order.price),
        'fees': str(order.fees),
        'total': str(order.total),
        'reconciled': str(int(order.reconciled)),
        'delta': str(order.get_delta()),
        'pl': str(order.get_pl())})
    return {'total': total, 'items': orders_return}
