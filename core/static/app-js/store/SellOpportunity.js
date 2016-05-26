Ext.define('semurg.store.SellOpportunity', {
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

  filters    : [{
      property: 'type',
      value   : 2
    }, {
      property: 'executed',
      value   : 0
  }],

  autoLoad   : true,
  remoteFilter: true,
  filterOnLoad: true,
  remoteSort : true
});
