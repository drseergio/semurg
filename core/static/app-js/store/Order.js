Ext.define('semurg.store.Order', {
  extend     : 'Ext.data.Store',
  model      : 'semurg.model.Order',

  proxy      : {
    type  : 'rest',
    url   : '/api/order',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  autoLoad   : true,
  remoteSort : false
});
