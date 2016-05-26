Ext.define('semurg.model.Position', {
  extend      : 'Ext.data.Model',
  fields      : [
      { name: 'id', type: 'int' },
      { name: 'symbol', type: 'string' },
      { name: 'quantity', type: 'int' },
      { name: 'orig', type: 'float' },
      { name: 'days', type: 'int' },
      { name: 'price', type: 'float' },
      { name: 'value', type: 'float' },
      { name: 'longterm', type: 'boolean' },
      { name: 'display', convert:
          function(v, rec) {
            return rec.get('symbol') + ' (' + rec.get('quantity') + ')'; }
          },
      { name: 'date', type: 'date', dateFormat: 'Y-m-d' },
      { name: 'delta_pct', type: 'float' },
      { name: 'delta', type: 'float' }],

  proxy       : {
    type: 'rest',
    url : '/api/position'
  }
});
