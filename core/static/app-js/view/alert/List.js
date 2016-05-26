Ext.define('semurg.view.alert.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.alertlist',
  border       : false,
  viewConfig   : {
    emptyText: '<div class="emptyText">No alerts defined..</div>',
    deferEmptyText: false,
  },
  initComponent: function() {
    this.selModel = Ext.create('Ext.selection.RowModel', {
      mode: 'MULTI'
    });
    this.columns = [{
        header      : 'Symbol',
        dataIndex   : 'symbol',
        flex        : 2,
        menuDisabled: true,
      }, {
        header      : 'Type',
        dataIndex   : 'type',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
      }, {
        header      : 'Current price',
        dataIndex   : 'price',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
      }, {
        header      : 'Target price',
        dataIndex   : 'target',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
        editor      : {
          allowBlank: false,
          hideTrigger: true,
          xtype     : 'numberfield',
          minValue  : 0.01,
          flex      : 2
        },
      }, {
        xtype       : 'checkcolumn',
        header      : 'Reached',
        dataIndex   : 'target_reached',
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
    this.store = 'Alert';
    this.tbar = [{
        text    : 'Add',
        action  : 'add',
        iconCls : 'icons-add',
      }, {
        text    : 'Delete',
        action  : 'delete',
        iconCls : 'icons-delete',
        disabled: true
    }];
    this.callParent(arguments);
  }
});
