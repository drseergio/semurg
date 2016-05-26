Ext.define('semurg.store.Position', {
  extend     : 'Ext.data.Store',
  model      : 'semurg.model.Position',

  proxy      : {
    type  : 'rest',
    url   : '/api/position',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  groupField : 'longterm',
  remoteGroup: true,
  autoLoad   : true,
  remoteSort : true
});
