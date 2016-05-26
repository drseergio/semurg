Ext.define('semurg.model.Alert', {
  extend      : 'Ext.data.Model',
  fields      : [
      { name: 'id', type: 'int' },
      { name: 'symbol', type: 'string' },
      { name: 'price', type: 'float' },
      { name: 'target', type: 'float' },
      { name: 'type', type: 'int' },
      { name: 'target_reached', type: 'boolean' }],

  proxy       : {
    type: 'rest',
    url : '/api/alert'
  }
});
