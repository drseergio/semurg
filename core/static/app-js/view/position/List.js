Ext.define('semurg.view.position.List', {
  extend       : 'Ext.grid.Panel',
  alias        : 'widget.positionlist',
  border       : false,
  viewConfig   : {
    emptyText: '<div class="emptyText">No positions yet..</div>',
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
        header      : 'Qty',
        dataIndex   : 'quantity',
        flex        : 1,
        menuDisabled: true,
      }, {
        header      : 'Days',
        dataIndex   : 'days',
        flex        : 1,
        menuDisabled: true,
      }, {
        xtype       : 'datecolumn',
        header      : 'Purchased',
        dataIndex   : 'date',
        format      : 'Y-m-d',
        flex        : 2,
        menuDisabled: true,
      }, {
        header      : 'Buy price',
        dataIndex   : 'orig',
        flex        : 2,
        menuDisabled: true,
      }, {
        header      : 'Price',
        dataIndex   : 'price',
        flex        : 2,
        menuDisabled: true,
      }, {
        header      : 'Current value',
        dataIndex   : 'value',
        flex        : 3,
        menuDisabled: true,
      }, {
        header      : 'Delta',
        dataIndex   : 'delta',
        flex        : 3,
        menuDisabled: true,
      }, {
        xtype       : 'actioncolumn',
        id          : 'action-column-position',
        flex        : 1,
        sortable    : false,
        menuDisabled: true,
        items       : [{
          iconCls: 'icons-income',
          tooltip: 'Sell',
        }]
    }];
    this.tbar = [{
        text    : 'New split',
        action  : 'split',
        iconCls : 'icons-split',
        disabled: true
      }, {
        xtype   : 'checkbox',
        boxLabel: 'Mark as long-term',
        name    : 'longterm',
        disabled: true
    }];
    this.store = 'Position';
    Ext.util.Format.term = function(val) {
      if (val) {
        return 'Long-term';
      } else {
        return 'Short-term';
      }
    }
    this.features = [Ext.create('Ext.grid.feature.Grouping', {
      groupHeaderTpl: '{name:term} ({rows.length} {[values.rows.length > 1 ? "items" : "item"]})'
    })];
    this.callParent(arguments);
  }
});
