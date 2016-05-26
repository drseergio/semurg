# -*- coding: utf-8 -*-
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from logging import getLogger
from settings import PROFIT_TARGET

logger = getLogger('core.models')


class Currency(models.Model):
  symbol = models.CharField(max_length=10)
  name = models.CharField(max_length=100, blank=True)
  code = models.CharField(max_length=10, blank=True)
  human = models.CharField(max_length=10, blank=True)
  unit = models.CharField(max_length=5)

  def __unicode__(self):
    return self.symbol


class CurrencyRate(models.Model):
  source = models.CharField(max_length=10)
  destination = models.CharField(max_length=10)
  rate = models.DecimalField(decimal_places=6, max_digits=30)
  last_update = models.DateTimeField()


class Instrument(models.Model):
  symbol = models.CharField(max_length=255, unique=True)
  exchange = models.CharField(max_length=255)
  currency = models.ForeignKey(Currency)
  close_price = models.DecimalField(decimal_places=2, max_digits=30)
  open_price = models.DecimalField(decimal_places=2, max_digits=30)
  last_price = models.DecimalField(decimal_places=2, max_digits=30)


class Position(models.Model):
  instrument = models.ForeignKey(Instrument)
  quantity = models.PositiveIntegerField()
  date = models.DateField()
  buy_price = models.DecimalField(decimal_places=2, max_digits=30)
  is_visible = models.BooleanField(default=True)
  is_longterm = models.BooleanField(default=False)

  def is_profit(self):
    if self.instrument.last_price >= (self.buy_price * Decimal(1.4)):
      return True
    return False


class Opportunity(models.Model):
  TYPE_BUY = 1
  TYPE_SELL = 2
  TYPE_SELL_T = 3

  TYPES = (
      (TYPE_BUY, 'Buy'),
      (TYPE_SELL, 'Sell (Profit)'),
      (TYPE_SELL_T, 'Sell (Time)'))

  symbol = models.CharField(max_length=255)
  date = models.DateField()
  breakout_date = models.DateField(blank=True, null=True)
  opportunity_type = models.IntegerField(max_length=2, choices=TYPES)
  is_executed = models.BooleanField(default=False)


class Breakout(models.Model):
  symbol = models.CharField(max_length=255)
  date = models.DateField()
  price = models.DecimalField(decimal_places=2, max_digits=30)
  reviewed = models.BooleanField(default=False)


class Watched(models.Model):
  instrument = models.ForeignKey(Instrument)
  create_date = models.DateField()
  synchronized = models.BooleanField(default=False)


class Alert(models.Model):
  TYPE_SMALLER = 1
  TYPE_GREATER = 2

  TYPES = (
      (TYPE_SMALLER, 'Smaller than'),
      (TYPE_GREATER, 'Greater than'))

  instrument = models.ForeignKey(Instrument)
  target = models.DecimalField(decimal_places=2, max_digits=30)
  target_reached = models.BooleanField(default=False)
  alert_type = models.IntegerField(max_length=2, choices=TYPES)


class Order(models.Model):
  instrument = models.ForeignKey(Instrument)
  quantity = models.PositiveIntegerField()
  date = models.DateField()
  price = models.DecimalField(decimal_places=2, max_digits=30)
  fees = models.DecimalField(decimal_places=2, max_digits=30)
  total = models.DecimalField(decimal_places=2, max_digits=30)
  position = models.ForeignKey(Position)
  opportunity = models.ForeignKey(Opportunity, blank=True, null=True)
  order_type = models.IntegerField(max_length=2, choices=Opportunity.TYPES)
  related_order = models.ForeignKey('self', null=True, blank=True)

  reconciled = models.BooleanField(default=False)
  synchronized = models.BooleanField(default=False)
  winning = models.BooleanField(default=False)
  profit_reached = models.BooleanField(default=False)

  def get_pl(self):
    if self.order_type == Opportunity.TYPE_BUY:
      return 'N/A'
    curr_value = self.price * self.quantity
    orig_value = self.related_order.price * self.related_order.quantity
    fees = self.fees + self.related_order.fees
    return curr_value - orig_value - fees

  def get_delta(self):
    if self.order_type == Opportunity.TYPE_BUY:
      return 'N/A'
    curr_value = self.price * self.quantity - self.fees - self.related_order.fees
    orig_value = self.related_order.price * self.related_order.quantity
    return round((curr_value-orig_value) / orig_value * 100, 2)

  def delete(self):
    if self.order_type == Opportunity.TYPE_BUY:
      try:
        related_order = Order.objects.get(related_order=self)
        transaction = Transaction.objects.get(order=related_order)
        transaction.delete()
      except ObjectDoesNotExist:
        pass
      self.position.delete()
    else:
      self.position.is_visible = True
      self.position.save()

    super(Order, self).delete()

  def save(self):
    if self.order_type != Opportunity.TYPE_BUY:
      if self.get_pl() > 0:
        self.winning = True
      else:
        self.winning = False
      if self.get_delta() >= (1 + PROFIT_TARGET) * 100:
        self.profit_reached = True
      else:
        self.profit_reached = False
    super(Order, self).save()


class Account(models.Model):
  balance = models.DecimalField(decimal_places=2, max_digits=30, default=0)
  currency = models.ForeignKey(Currency)

  def add_balance(self, amount, transaction_type):
    if not Transaction.is_add(transaction_type):
      amount *= -1
    self.balance += amount
    self.save()

  def del_balance(self, amount, transaction_type):
    if not Transaction.is_add(transaction_type):
      amount *= -1
    self.balance -= amount
    self.save()

  def change_balance(self, old_amount, new_amount, transaction_type):
    if not Transaction.is_add(transaction_type):
      new_amount *= -1
      old_amount *= -1
    self.balance -= old_amount
    self.balance += new_amount
    self.save()


class Transaction(models.Model):
  TYPE_BUY = 1
  TYPE_SELL = 2
  TYPE_WITHDRAWAL = 3
  TYPE_DEPOSIT = 4

  TYPES = (
      (TYPE_BUY, 'Buy'),
      (TYPE_SELL, 'Sell'),
      (TYPE_WITHDRAWAL, 'Withdrawal'),
      (TYPE_DEPOSIT, 'Deposit'))

  amount = models.DecimalField(decimal_places=2, max_digits=30)
  date = models.DateField()
  description = models.TextField(blank=True)
  reconciled = models.BooleanField(default=False)
  order = models.ForeignKey(Order, blank=True, null=True)
  transaction_type = models.IntegerField(max_length=2, choices=TYPES)

  @classmethod
  def is_add(self, transaction_type):
    if (transaction_type == Transaction.TYPE_SELL or
        transaction_type == Transaction.TYPE_DEPOSIT):
      return True
    return False

  def delete(self):
    account = Account.objects.get(id=1)
    account.del_balance(self.amount, self.transaction_type)
    order = self.order

    super(Transaction, self).delete()

    if order:
      order.delete()

  def save(self):
    account = Account.objects.get(id=1)
    if not self.id:
      account.add_balance(self.amount, self.transaction_type)
    else:
      old_self = Transaction.objects.get(id=self.id)
      account.change_balance(old_self.amount, self.amount, self.transaction_type)
    super(Transaction, self).save()
