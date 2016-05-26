Ext.define('semurg.model.Opportunity', {
  extend      : 'Ext.data.Model',
  fields      : [
      { name: 'id', type: 'int' },
      { name: 'symbol', type: 'string' },
      { name: 'type', type: 'int' },
      { name: 'quantity', type: 'int' },
      { name: 'period', type: 'string' },
      { name: 'price', type: 'float' },
      { name: 'amount', type: 'float' },
      { name: 'executed', type: 'int' },
      { name: 'breakout_date', type: 'string' },
      { name: 'date', type: 'date', dateFormat: 'Y-m-d' }],

  proxy       : {
    type: 'rest',
    url : '/api/opportunity'
  }
});
