Ext.define('semurg.view.transaction.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.transactionlist',
  border       : false,
  viewConfig   : {
    emptyText: '<div class="emptyText">No transactions yet..</div>',
    deferEmptyText: false,
  },
  initComponent: function() {
    this.selModel = Ext.create('Ext.selection.RowModel', {
      mode: 'MULTI'
    });
    this.columns = [{
        xtype       : 'datecolumn',
        header      : 'Date',
        dataIndex   : 'date',
        format      : 'Y-m-d',
        flex        : 2,
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
        menuDisabled: true,
      }, {
        header      : 'Description',
        dataIndex   : 'description',
        flex        : 4,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          flex: 4
        }
      }, {
        header      : 'Amount',
        dataIndex   : 'amount',
        flex        : 2,
        menuDisabled: true,
        editor      : {
          allowBlank: false,
          xtype     : 'numberfield',
          minValue  : 0.01,
          flex      : 2
        },
      }, {
        xtype       : 'checkcolumn',
        header      : 'RC\'ed',
        dataIndex   : 'reconciled',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
     }
    ];
    this.plugins = [
        Ext.create('Ext.grid.plugin.RowEditing', {
          clicksToMoveEditor: 1,
          autoCancel        : false,
          pluginId          : 'rowEditing'
        })];
    this.store = 'Transaction';
    this.tbar = [{
        text    : 'Deposit',
        action  : 'deposit',
        iconCls : 'icons-income',
      }, {
        text    : 'Withdraw',
        action  : 'withdraw',
        iconCls : 'icons-expense',
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
      }, {
        text    : 'Import csv',
        action  : 'import',
        iconCls : 'icons-import'
      }, {
        text    : 'Export csv',
        action  : 'export',
        iconCls : 'icons-export'
    }];
    this.bbar = Ext.create('Ext.PagingToolbar', ({
      store      : 'Transaction',
      displayInfo: true,
      displayMsg : 'Displaying transactions {0} - {1} of {2}',
      emptyMsg   : "No transactions to display",
    }));
    this.callParent(arguments);
  }
});
