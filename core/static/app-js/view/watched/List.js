Ext.define('semurg.view.watched.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.watchlist',
  border       : false,
  viewConfig   : {
    emptyText: '<div class="emptyText">Not following anything..</div>',
    deferEmptyText: false,
    plugins: {
      ptype: 'gridviewdragdrop',
      dropGroup: 'breakoutDDGroup'
    },
  },
  initComponent: function() {
    this.columns = [{
        header      : 'Symbol',
        dataIndex   : 'symbol',
        flex        : 2,
        menuDisabled: true,
      }, {
        header      : 'Price',
        dataIndex   : 'price',
        flex        : 2,
        menuDisabled: true,
      }, {
        xtype       : 'datecolumn',
        header      : 'Added',
        dataIndex   : 'date',
        format      : 'Y-m-d',
        flex        : 2,
        menuDisabled: true,
      }, {
        xtype       : 'actioncolumn',
        id          : 'action-column-watched',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        items       : [{
          iconCls: 'icons-delete',
          tooltip: 'Delete',
        }, {
          iconCls: 'icons-bell',
          tooltip: 'Create alert',
        }]
    }];
    this.store = 'Watched';
    this.tbar = [{
        text    : 'Add',
        action  : 'add',
        iconCls : 'icons-add',
    }];
    this.callParent(arguments);
  }
});
