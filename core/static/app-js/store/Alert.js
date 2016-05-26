Ext.define('semurg.store.Alert', {
  extend     : 'Ext.data.Store',
  model      : 'semurg.model.Alert',

  proxy      : {
    type  : 'rest',
    url   : '/api/alert',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  autoLoad   : true,
  remoteSort : true
});
