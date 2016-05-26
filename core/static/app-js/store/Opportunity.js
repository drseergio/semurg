Ext.define('semurg.store.Opportunity', {
  extend     : 'Ext.data.Store',
  model      : 'semurg.model.Opportunity',

  proxy      : {
    type  : 'rest',
    url   : '/api/opportunity',
    reader: {
      type : 'json',
      root : 'items',
    }
  },

  groupField : 'period',
  remoteGroup: true,
  autoLoad   : true,
  remoteSort : true
});
