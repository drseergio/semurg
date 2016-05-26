Ext.define('semurg.controller.Position', {
  extend          : 'Ext.app.Controller',
  views           : [ 'position.List' ],
  stores          : [ 'Position' ],
  models          : [ 'Position' ],

  refs: [{
      selector: 'positionlist',
      ref     : 'positionList'
  }],

  init            : function() {
    this.control({
      'positionlist'                       : {
        selectionchange: this.onSelectionChange,
        render         : this.onRender,
      },
      'positionlist checkbox'              : {
        change         : this.onCheckbox
      },
      'positionlist button[action=split]'  : {
        click          : this.openSplit
      },
      'actioncolumn#action-column-position': {
        click          : this.onColumnAction
      },
    });

    this.application.on({
      scope            : this
    });
  },

  onRender: function(list) {
    column = list.down('[dataIndex=orig]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=price]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=value]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=delta]');
    column.renderer = this.deltaRenderer;
    column = list.down('[dataIndex=symbol]');
    column.renderer = this.symbolRenderer;
  },

  onColumnAction: function(grid, cell, row, col, e) {
    var rec = grid.getStore().getAt(row);
    var action = e.target.getAttribute('class');

    if (action.indexOf('x-action-col-0') != -1) {
      var tabpanel = Ext.ComponentQuery.query("#app-center")[0];
      tabpanel.setActiveTab("app-center-order");
      var orderController = this.application.getController('Order');
      orderController.openAddOrder(2, rec);
    }
  },

  onSelectionChange  : function(model, record, index) {
    var win = this.getPositionList();
    var longterm = win.down('checkbox');
    var split = win.down('button[action=split]');

    if (model.hasSelection()) {
      if (model.getCount() == 1) {
        split.enable();
      } else {
        split.disable();
      }
      var has_longterm = false;
      model.getSelection().forEach(function(item) {
        if (item.get('longterm')) {
          has_longterm = true;
        }
      });
      longterm.enable();
      if (has_longterm != longterm.getValue()) {
        this.enable_checkbox = true;  // hack to prevent ExtJS from firing event
        longterm.setValue(has_longterm);
      }
    } else {
      split.disable();
      longterm.disable();
    }
  },

  onCheckbox: function(field, new_value, old_value, ee) {
    if (this.enable_checkbox) {
      this.enable_checkbox = false;
      return;
    }

    var model = this.getPositionList().getSelectionModel();
    var store = this.getPositionStore();
    model.getSelection().forEach(function(item) {
      item.set('longterm', new_value);
    });

    store.mySync({
      scope   : this,
      callback: function() {
      }
    });
  },

  amountRenderer: function(value, metaData, record) {
    return formatted = Ext.util.Format.currency(value);
  },

  deltaRenderer: function(value, metaData, record) {
    var pct = Math.abs(record.get('delta_pct')) * 100;
    var formatted = Ext.util.Format.currency(value);

    if (value < 0) {
      return '<span style="color:red;">' + formatted + ' (' + pct.toFixed(2) + '%)</span>';
    } else {
      return '<span style="color:green;">' + formatted + ' (' + pct.toFixed(2) + '%)</span>';
    }
  },

  symbolRenderer: function(value, metaData, record) {
    return '<a target="_blank" href="http://finance.yahoo.com/q?s='+ value +'">' + value + '</a>';
  },

  openSplit: function() {
    var me = this;
    Ext.MessageBox.prompt('New quantity', 'Please input new quantity (post split)', function(btn, text) {
      if (btn != 'cancel') {
        var win = me.getPositionList();
        var model = win.getSelectionModel();
        var position = model.getLastSelected();
        var store = me.getPositionStore();
        position.set('quantity', text);
        position.save({
          success: function(rec, op) {
            store.load();
          }
        });
      }
    });
  }
});
