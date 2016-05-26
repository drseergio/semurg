Ext.define('semurg.view.opportunity.SellList', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.opportunityselllist',
  border       : false,
  viewConfig   : {
    emptyText: '<div class="emptyText">No more opportunities today</div>',
    deferEmptyText: false,
    plugins: {
      ptype    : 'gridviewdragdrop',
      dragGroup: 'opportunityDDGroup'
    }
  },
  initComponent: function() {
    this.columns = [{
        header      : 'Symbol',
        dataIndex   : 'symbol',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
      }, {
        header      : 'Price',
        dataIndex   : 'price',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
      }, {
        header      : 'Type',
        dataIndex   : 'type',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
    }];
    this.store = 'SellOpportunity';
    this.callParent(arguments);
  }
});
