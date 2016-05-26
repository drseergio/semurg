# -*- coding: utf-8 -*-
from core.forms import SemurgForm
from core.logic import get_instrument
from core.logic.order import create_buy_order
from core.logic.order import create_sell_order
from core.models import Currency
from core.models import Instrument
from core.models import Opportunity
from core.models import Order
from core.models import Position
from core.models import Transaction
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.forms import BooleanField
from django.forms import CharField
from django.forms import ChoiceField
from django.forms import DateField
from django.forms import DecimalField
from django.forms import IntegerField
from django.forms import ModelChoiceField
from django.forms import ValidationError
from logging import getLogger

logger = getLogger('core.forms.order')


class OrderAddForm(SemurgForm):
  type = ChoiceField(choices=Opportunity.TYPES)
  date = DateField(initial=datetime.utcnow())
  price = DecimalField(initial=0.0)
  fees = DecimalField(initial=0.0)
  total = DecimalField(initial=0.0)
  opportunity = ModelChoiceField(queryset=Opportunity.objects.all(), required=False)

  def clean_total(self):
    return self._check_amount('total')

  def clean_price(self):
    return self._check_amount('price')

  def clean_fees(self):
    return self._check_amount('fees')

  def _check_amount(self, field):
    amount = self.cleaned_data[field]
    if amount and amount <= 0:
      raise ValidationError(
          'Amount cannot be negative')
    return amount


class OrderBuyForm(OrderAddForm):
  quantity = IntegerField(min_value=1)
  symbol = CharField()

  def clean_symbol(self):
    symbol = self.cleaned_data['symbol']
    try:
      instrument = get_instrument(symbol)
    except:
      raise ValidationError('Instrument does not exist and sync failed')
    return instrument

  def save(self):
    return create_buy_order(self.cleaned_data)


class OrderSellForm(OrderAddForm):
  def __init__(self, *args, **kwargs):
    super(OrderSellForm, self).__init__(*args, **kwargs)
    self.fields['position_id'] = ModelChoiceField(queryset=Position.objects.filter(is_visible=True))

  def save(self):
    return create_sell_order(self.cleaned_data)


class OrderEditForm(SemurgForm):
  reconciled = BooleanField(required=False)
  quantity = IntegerField(min_value=1)
  fees = DecimalField(initial=0.0)
  price = DecimalField(initial=0.0)
  total = DecimalField(initial=0.0)

  def __init__(self, *args, **kwargs):
    super(OrderEditForm, self).__init__(*args, **kwargs)
    self.fields['id'] = ModelChoiceField(queryset=Order.objects.all())

  def clean_total(self):
    return self._check_amount('total')

  def clean_price(self):
    return self._check_amount('price')

  def clean_fees(self):
    return self._check_amount('fees')

  def clean(self):
    super(OrderEditForm, self).clean()
    cleaned_data = self.cleaned_data
    order = cleaned_data['id']
    if order.reconciled:
      self.add_error('price', 'Reconciled order cannot be changed')
    return cleaned_data

  def save(self):
    order = self.cleaned_data['id']
    order.reconciled = self.cleaned_data['reconciled']
    order.quantity = self.cleaned_data['quantity']
    order.fees = self.cleaned_data['fees']
    order.price = self.cleaned_data['price']
    order.total = self.cleaned_data['total']
    order.save()
    transaction = Transaction.objects.get(order=order)
    transaction.amount = order.total
    transaction.save()

  def _check_amount(self, field):
    amount = self.cleaned_data[field]
    if amount and amount <= 0:
      raise ValidationError(
          'Amount cannot be negative')
    return amount
