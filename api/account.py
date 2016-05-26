# -*- coding: utf-8 -*-
from api import get_paged
from api import load_params
from api.decorators import require_args
from api.decorators import require_pager
from core.forms.account import TransactionAddForm
from core.forms.account import TransactionEditForm
from core.logic import is_market_open
from core.logic import get_portfolio_delta
from core.logic.position import get_total_equity
from core.models import Account
from core.models import Transaction
from datetime import date
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.db import transaction
from logging import getLogger
from piston.handler import BaseHandler
from piston.utils import rc
from settings import GULLWING_VERSION
from settings import VERSION

logger = getLogger('api.transaction')


class AccountHandler(BaseHandler):
  model = Account

  def read(self, request):
    account = Account.objects.all()[0]
    delta, pct = get_portfolio_delta()
    return {
        'open': int(is_market_open()),
        'delta': str(delta),
        'version': VERSION,
        'gullwing_version': GULLWING_VERSION,
        'pct': str(pct),
        'date': str(date.today()),
        'equity': get_total_equity(),
        'cash': account.balance }


class TransactionHandler(BaseHandler):
  model = Transaction

  @require_args(['limit', 'start'], 'GET')
  @require_pager
  def read(self, request):
    start = int(request.GET['start'])
    limit = int(request.GET['limit'])

    transactions = Transaction.objects.all().order_by('-date')
    paged_transactions = get_paged(transactions, start, limit)

    return self._handle_transactions(paged_transactions, len(transactions))

  @transaction.commit_on_success
  def create(self, request, *args, **kwargs):
    params = load_params(request)

    form = TransactionAddForm(params)
    if form.is_valid():
      transaction = form.save()
      return {'success': True, 'id': transaction.id}
    else:
      return {'success': False, 'errors': form.get_errors()}

  @transaction.commit_on_success
  def delete(self, request, transaction_id):
    transaction = Transaction.objects.get(
        id=transaction_id)
    if transaction.reconciled:
      return {'success': False}
    else:
      transaction.delete()
      return {'success': True}

  @transaction.commit_on_success
  def update(self, request, transaction_id):
    params = load_params(request)
    params['id'] = transaction_id

    form = TransactionEditForm(params)
    if form.is_valid():
      form.save()
      return {'success': True}
    else:
      return {'success': False, 'errors': form.get_errors()}

  def _handle_transactions(self, transactions, total):
    transactions_return = []
    for transaction in transactions:
      transactions_return.append({
        'id': transaction.id,
        'date': str(transaction.date),
        'amount': str(abs(transaction.amount)),
        'reconciled': str(int(transaction.reconciled)),
        'type': transaction.transaction_type,
        'description': transaction.description})
    return {'total': total, 'items': transactions_return}
