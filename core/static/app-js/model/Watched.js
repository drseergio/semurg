Ext.define('semurg.model.Watched', {
  extend      : 'Ext.data.Model',
  fields      : [
      { name: 'id', type: 'int' },
      { name: 'symbol', type: 'string' },
      { name: 'price', type: 'float' },
      { name: 'date', type: 'date', dateFormat: 'Y-m-d' }],

  proxy       : {
    type: 'rest',
    url : '/api/watched'
  }
});
