Ext.define('semurg.model.Transaction', {
  extend      : 'Ext.data.Model',
  fields      : [
      { name: 'id', type: 'int' },
      { name: 'date', type: 'date', dateFormat: 'Y-m-d' },
      { name: 'amount', type: 'float' },
      { name: 'description', type: 'string' },
      { name: 'reconciled', type: 'boolean' },
      { name: 'type', type: 'int' }],

  proxy       : {
    type: 'rest',
    url : '/api/transaction'
  }
});
