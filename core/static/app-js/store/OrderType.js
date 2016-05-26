Ext.define('semurg.store.OrderType', {
  extend: 'Ext.data.Store',
  fields: ['value', 'text'],
  data  : [{
      'text'  : 'Buy',
      'value': 1
    }, {
      'text'  : 'Sell (P)',
      'value': 2
    }, {
      'text'  : 'Sell (T)',
      'value': 3
  }]
});
