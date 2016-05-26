Ext.define('semurg.store.Watched', {
  extend     : 'Ext.data.Store',
  model      : 'semurg.model.Watched',

  proxy      : {
    type  : 'rest',
    url   : '/api/watched',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  autoLoad   : true,
  remoteSort : true
});
