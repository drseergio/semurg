Ext.define('semurg.store.Breakout', {
  extend     : 'Ext.data.Store',
  model      : 'semurg.model.Breakout',

  proxy      : {
    type  : 'rest',
    url   : '/api/breakout',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  groupField : 'date',
  remoteGroup: true,
  autoLoad   : true,
  remoteSort : true
});
