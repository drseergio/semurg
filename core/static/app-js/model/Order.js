Ext.define('semurg.model.Order', {
  extend      : 'Ext.data.Model',
  fields      : [
      { name: 'id', type: 'int' },
      { name: 'symbol', type: 'string' },
      { name: 'date', type: 'date', dateFormat: 'Y-m-d' },
      { name: 'type', type: 'int' },
      { name: 'quantity', type: 'int' },
      { name: 'price', type: 'float' },
      { name: 'fees', type: 'float' },
      { name: 'total', type: 'float' },
      { name: 'reconciled', type: 'boolean' },
      { name: 'delta', type: 'string' },
      { name: 'opportunity', type: 'int' },
      { name: 'pl', type: 'string' }],

  proxy       : {
    type: 'rest',
    url : '/api/order'
  }
});
