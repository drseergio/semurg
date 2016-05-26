Ext.define('semurg.controller.Breakout', {
  extend          : 'Ext.app.Controller',
  views           : [
      'breakout.List' ],
  stores          : [ 'Breakout' ],
  models          : [ 'Breakout' ],

  refs: [{
      selector: 'breakoutlist',
      ref     : 'breakoutList'
  }],

  init            : function() {
    this.control({
      'breakoutlist'                       : {
        render         : this.onRender,
        selectionchange: this.onSelectionChange,
      },
      'breakoutlist button[action=review]' : {
        click: this.reviewBreakouts
      },
      'actioncolumn#action-column-breakout': {
        click          : this.onColumnAction
      },
    });

    this.application.on({
      scope            : this
    });
  },

  onRender: function(list) {
    column = list.down('[dataIndex=price]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=symbol]');
    column.renderer = this.symbolRenderer;
  },

  onColumnAction: function(grid, cell, row, col, e) {
    var rec = grid.getStore().getAt(row);
    var action = e.target.getAttribute('class');

    if (action.indexOf('x-action-col-0') != -1) {
      this.getController('Alert').openAddAlert(rec.get('symbol'));
    }
  },

  onSelectionChange  : function(model, record, index) {
    var win = this.getBreakoutList();
    var review = win.down('button[action=review]');

    if (model.hasSelection()) {
      review.enable();
    } else {
      review.disable();
    }
  },

  reviewBreakouts: function() {
    var list = this.getBreakoutList();
    var model = list.getSelectionModel();
    var selected = model.getSelection();
    var store = this.getBreakoutStore();

    selected.forEach(function(order) {
      order.set('reviewed', true);
    });

    store.mySync({
      scope   : this,
      callback: function() {
        store.load();
      }
    });

    this.application.fireEvent('reviewbreakouts');
  },

  amountRenderer: function(value, metaData, record) {
    return Ext.util.Format.currency(value);
  },

  symbolRenderer: function(value, metaData, record) {
    return '<a target="_blank" href="http://finance.yahoo.com/q?s='+ value +'">' + value + '</a>';
  },
});
