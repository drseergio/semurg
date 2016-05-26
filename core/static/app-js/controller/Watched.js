Ext.define('semurg.controller.Watched', {
  extend          : 'Ext.app.Controller',
  views           : [ 'watched.List' ],
  stores          : [ 'Watched' ],
  models          : [ 'Watched' ],

  refs: [{
      selector: 'watchlist',
      ref     : 'watchList'
  }],

  init            : function() {
    this.control({
      'watchlist'                   : {
        render         : this.onRender,
      },
      'watchlist button[action=add]': {
        click: this.addWatch
      },
      'watchlist dataview'          : {
        beforedrop     : this.onBeforeDrop,
      },
      'actioncolumn#action-column-watched': {
        click          : this.onColumnAction
      },
    });

    this.application.on({
      scope            : this,
      addwatch         : this.onAddWatch
    });
  },

  onRender: function(list) {
    column = list.down('[dataIndex=price]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=symbol]');
    column.renderer = this.symbolRenderer;
  },

  onBeforeDrop: function(node, data) {
    var breakout = data.records[0];
    var symbol = breakout.get('symbol');
    this.createWatch(symbol);
    return false;
  },

  onAddWatch: function(symbol) {
    Ext.example.msg(
        'Created watch',
        'Successfully created watch for ' + symbol);
  },

  onColumnAction: function(grid, cell, row, col, e) {
    var rec = grid.getStore().getAt(row);
    var store = this.getWatchedStore();
    var action = e.target.getAttribute('class');

    if (action.indexOf('x-action-col-0') != -1) {
      rec.destroy({
        success: function() {
          store.load();
        }
      });
    }
    if (action.indexOf('x-action-col-1') != -1) {
      this.getController('Alert').openAddAlert(rec.get('symbol'));
    }
  },

  addWatch: function() {
    var me = this;
    Ext.MessageBox.prompt('Symbol', 'Please enter symbol to follow', function(btn, text) {
      if (btn != 'cancel') {
        me.createWatch(text);
      }
    });
  },

  createWatch: function(symbol) {
    var watch = Ext.create('semurg.model.Watched', {
      symbol: symbol
    });
    var store = this.getWatchedStore();
    var app = this.application;
    watch.save({
      success: function(rec, op) {
        store.load();
        app.fireEvent('addwatch', symbol);
      },
      failure: function(rec, op) {
        Ext.example.msg(
          'Failed',
          'Failed to create watch for ' + symbol);
      }
    });
  },

  amountRenderer: function(value, metaData, record) {
    return Ext.util.Format.currency(value);
  },

  symbolRenderer: function(value, metaData, record) {
    return '<a target="_blank" href="http://finance.yahoo.com/q?s='+ value +'">' + value + '</a>';
  },
});
