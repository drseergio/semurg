Ext.define('semurg.store.TransactionType', {
  extend: 'Ext.data.Store',
  fields: ['value', 'text'],
  data  : [{
      'text'  : 'Buy',
      'value': 1
    }, {
      'text'  : 'Sell',
      'value': 2
    }, {
      'text'  : 'Withdrawal',
      'value': 3
    }, {
      'text'  : 'Deposit',
      'value': 4
  }]
});
