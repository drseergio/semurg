Ext.define('semurg.view.opportunity.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.opportunitylist',
  border       : false,
  viewConfig   : {
    emptyText: '<div class="emptyText">No opportunities yet..</div>',
    deferEmptyText: false,
    plugins: {
      ptype    : 'gridviewdragdrop',
      dragGroup: 'breakoutDDGroup'
    }
  },
  initComponent: function() {
    this.columns = [{
        header      : 'Symbol',
        dataIndex   : 'symbol',
        flex        : 2,
        menuDisabled: true,
      }, {
        header      : 'Type',
        dataIndex   : 'type',
        flex        : 2,
        menuDisabled: true,
      }, {
        header      : 'Price',
        dataIndex   : 'price',
        flex        : 2,
        menuDisabled: true,
      }, {
        header      : 'Suggested Qty',
        dataIndex   : 'quantity',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
      }, {
        header      : 'Suggested Total',
        dataIndex   : 'amount',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
      }, {
        xtype       : 'datecolumn',
        header      : 'Date',
        dataIndex   : 'date',
        format      : 'Y-m-d',
        flex        : 2,
        menuDisabled: true,
      }, {
        header      : 'Breakout',
        dataIndex   : 'breakout_date',
        flex        : 2,
        menuDisabled: true,
      }, {
        xtype       : 'actioncolumn',
        id          : 'action-column-opportunity',
        flex        : 3,
        sortable    : false,
        menuDisabled: true,
        items       : [{
          iconCls: 'icons-commit',
          tooltip: 'Execute',
        }, {
          iconCls: 'icons-chart',
          tooltip: 'Break-out chart',
        }, {
          iconCls: 'icons-bell',
          tooltip: 'Create alert',
        }]
      }, {
        xtype       : 'checkcolumn',
        header      : 'Executed',
        dataIndex   : 'executed',
        flex        : 2,
        menuDisabled: true,
    }];
    this.features = [Ext.create('Ext.grid.feature.Grouping', {
      groupHeaderTpl: '{name} ({rows.length} {[values.rows.length > 1 ? "items" : "item"]})'
    })];
    this.store = 'Opportunity';
    this.bbar = Ext.create('Ext.PagingToolbar', ({
      store      : 'Opportunity',
      displayInfo: true,
      displayMsg : 'Displaying opportunities {0} - {1} of {2}',
      emptyMsg   : "No transactions to display",
    }));
    this.callParent(arguments);
  }
});
