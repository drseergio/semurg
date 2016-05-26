Ext.define('semurg.store.BuyOpportunity', {
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
      value   : 1
    }, {
      property: 'executed',
      value   : 0
  }],

  autoLoad    : true,
  remoteFilter: true,
  filterOnLoad: true,
  remoteSort  : true
});
