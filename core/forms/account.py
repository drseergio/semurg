# -*- coding: utf-8 -*-
from core.forms import SemurgForm
from core.models import Transaction
from datetime import datetime
from django.forms import BooleanField
from django.forms import CharField
from django.forms import ChoiceField
from django.forms import DateField
from django.forms import DecimalField
from django.forms import ModelChoiceField
from logging import getLogger

logger = getLogger('core.forms.account')


class TransactionAddForm(SemurgForm):
  type = ChoiceField(choices=Transaction.TYPES[2:4])
  description = CharField(required=False)
  amount = DecimalField(initial=0.0)
  date = DateField(initial=datetime.utcnow())

  def clean_amount(self):
    amount = self.cleaned_data['amount']
    if amount and amount <= 0:
      raise ValidationError(
          'Amount cannot be negative')
    return amount

  def save(self):
    transaction_type = int(self.cleaned_data['type'])
    date = self.cleaned_data['date']
    description = self.cleaned_data['description']
    amount = self.cleaned_data['amount']

    transaction = Transaction(
        transaction_type=transaction_type,
        date=date,
        description=description,
        amount=amount)
    transaction.save()
    return transaction


class TransactionEditForm(SemurgForm):
  description = CharField(required=False)
  amount = DecimalField(initial=0.0)
  date = DateField()
  reconciled = BooleanField(required=False)

  def __init__(self, *args, **kwargs):
    super(TransactionEditForm, self).__init__(*args, **kwargs)
    self.fields['id'] = ModelChoiceField(queryset=Transaction.objects.all())

  def clean_amount(self):
    amount = self.cleaned_data['amount']
    if amount and amount <= 0:
      raise ValidationError(
          'Amount cannot be negative')
    return amount

  def clean(self):
    super(TransactionEditForm, self).clean()
    cleaned_data = self.cleaned_data
    transaction = cleaned_data['id']
    if transaction.reconciled:
      self.add_error('amount', 'Reconciled transactions cannot be changed')
    return cleaned_data

  def save(self):
    transaction = self.cleaned_data['id']
    transaction.date = self.cleaned_data['date']
    transaction.amount = self.cleaned_data['amount']
    transaction.reconciled = self.cleaned_data['reconciled']
    transaction.description = self.cleaned_data['description']
    if transaction.order:
      transaction.order.total = transaction.amount
      transaction.order.save()
    transaction.save()
