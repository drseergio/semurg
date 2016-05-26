Ext.define('semurg.model.Breakout', {
  extend      : 'Ext.data.Model',
  fields      : [
      { name: 'id', type: 'int' },
      { name: 'symbol', type: 'string' },
      { name: 'reviewed', type: 'boolean' },
      { name: 'price', type: 'float' },
      { name: 'date', type: 'date', dateFormat: 'Y-m-d' }],

  proxy       : {
    type: 'rest',
    url : '/api/breakout'
  }
});
