Ext.define('semurg.store.AlertType', {
  extend: 'Ext.data.Store',
  fields: ['value', 'text'],
  data  : [{
      'text'  : 'Smaller than',
      'value': 1
    }, {
      'text'  : 'Greater than',
      'value': 2
  }]
});
