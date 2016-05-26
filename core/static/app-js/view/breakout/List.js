Ext.define('semurg.view.breakout.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.breakoutlist',
  border       : false,
  viewConfig   : {
    getRowClass: function(record, index) {
      var c = record.get('reviewed');
      if (c) {
        return 'breakout-reviewed';
      } else {
        return '';
      }
    },
    emptyText: '<div class="emptyText">No breakouts yet..</div>',
    deferEmptyText: false,
    plugins: {
      ptype    : 'gridviewdragdrop',
      dragGroup: 'breakoutDDGroup'
    }
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
        xtype       : 'datecolumn',
        header      : 'Date',
        dataIndex   : 'date',
        format      : 'Y-m-d',
        flex        : 2,
        menuDisabled: true,
      }, {
        header      : 'Close price',
        dataIndex   : 'price',
        flex        : 2,
        menuDisabled: true,
      }, {
        xtype       : 'actioncolumn',
        id          : 'action-column-breakout',
        flex        : 2,
        sortable    : false,
        menuDisabled: true,
        items       : [{
          iconCls: 'icons-bell',
          tooltip: 'Create alert',
        }]
    }];
    this.features = [Ext.create('Ext.grid.feature.Grouping', {
      groupHeaderTpl: '{name:date("Y-m-d")} ({rows.length} {[values.rows.length > 1 ? "items" : "item"]})'
    })];
    this.store = 'Breakout';
    this.tbar = [{
        text    : 'Mark reviewed',
        action  : 'review',
        iconCls : 'icons-review',
        disabled: true
    }];
    this.bbar = Ext.create('Ext.PagingToolbar', ({
      store      : 'Breakout',
      displayInfo: true,
      displayMsg : 'Displaying breakouts {0} - {1} of {2}',
      emptyMsg   : "No breakouts to display",
    }));
    this.callParent(arguments);
  }
});
