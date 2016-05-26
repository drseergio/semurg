Ext.define('semurg.store.Transaction', {
  extend     : 'Ext.data.Store',
  model      : 'semurg.model.Transaction',

  proxy      : {
    type  : 'rest',
    url   : '/api/transaction',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  remoteSort : false,
  autoLoad   : true
});
