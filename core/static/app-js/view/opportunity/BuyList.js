Ext.define('semurg.view.opportunity.BuyList', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.opportunitybuylist',
  border       : false,
  multiSelect  : true,
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
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
      }, {
        header      : 'Price',
        dataIndex   : 'price',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
      }, {
        xtype       : 'datecolumn',
        header      : 'Date',
        dataIndex   : 'date',
        format      : 'Y-m-d',
        flex        : 1,
        menuDisabled: true,
    }];
    this.store = 'BuyOpportunity';
    this.callParent(arguments);
  }
});
