Ext.define('semurg.view.order.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.orderlist',
  border       : false,
  viewConfig   : {
    emptyText: '<div class="emptyText">No orders yet..</div>',
    deferEmptyText: false,
    plugins: {
      ptype: 'gridviewdragdrop',
      dropGroup: 'opportunityDDGroup'
    },
  },
  initComponent: function() {
    this.selModel = Ext.create('Ext.selection.RowModel', {
      mode: 'MULTI'
    });
    this.columns = [{
        header      : 'Symbol',
        dataIndex   : 'symbol',
        flex        : 1,
        menuDisabled: true,
      }, {
        xtype       : 'datecolumn',
        header      : 'Date',
        dataIndex   : 'date',
        format      : 'Y-m-d',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          xtype     : 'datefield',
          flex      : 2,
          format    : 'Y-m-d',
          allowBlank: false
        }
      }, {
        header      : 'Type',
        dataIndex   : 'type',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
      }, {
        header      : 'Qty',
        dataIndex   : 'quantity',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          allowBlank: false,
          xtype     : 'numberfield',
          minValue  : 1,
          hideTrigger: true,
          flex      : 1
        },
      }, {
        header      : 'Fees',
        dataIndex   : 'fees',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          allowBlank: false,
          xtype     : 'numberfield',
          hideTrigger: true,
          minValue  : 0,
          flex      : 1
        },
      }, {
        header      : 'Price',
        dataIndex   : 'price',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          allowBlank: false,
          xtype     : 'numberfield',
          hideTrigger: true,
          minValue  : 0.01,
          flex      : 1
        },
      }, {
        header      : 'Total',
        dataIndex   : 'total',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          allowBlank: false,
          hideTrigger: true,
          xtype     : 'numberfield',
          minValue  : 0,
          flex      : 2
        },
      }, {
        header      : 'P/L',
        dataIndex   : 'pl',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
      }, {
        header      : 'Delta',
        dataIndex   : 'delta',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
      }, {
        xtype       : 'checkcolumn',
        header      : 'RC\'ed',
        dataIndex   : 'reconciled',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
     }
    ];
    this.plugins = [Ext.create('Ext.grid.plugin.RowEditing', {
        clicksToMoveEditor: 1,
        autoCancel        : false,
        pluginId          : 'rowEditing'
      })];
    this.store = 'Order';
    this.tbar = [{
        text    : 'Buy',
        action  : 'buy',
        iconCls : 'icons-add',
      }, {
        text    : 'Sell',
        action  : 'sell',
        iconCls : 'icons-income',
      }, {
        text    : 'Delete',
        action  : 'delete',
        iconCls : 'icons-delete',
        disabled: true
      }, {
        text    : 'Reconcile',
        action  : 'reconcile',
        iconCls : 'icons-reconcile',
        disabled: true
    }];
    this.bbar = Ext.create('Ext.PagingToolbar', ({
      store      : 'Order',
      displayInfo: true,
      displayMsg : 'Displaying orders {0} - {1} of {2}',
      emptyMsg   : "No orders to display",
    }));
    this.callParent(arguments);
  }
});
