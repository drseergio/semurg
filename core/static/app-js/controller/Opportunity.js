Ext.define('semurg.controller.Opportunity', {
  extend          : 'Ext.app.Controller',
  views           : [
      'opportunity.BuyList',
      'opportunity.List',
      'opportunity.SellList' ],
  stores          : [
      'BuyOpportunity',
      'Opportunity',
      'OrderType',
      'SellOpportunity' ],
  models          : [ 'Opportunity', 'Opportunity' ],

  refs: [{
      selector: 'opportunitylist',
      ref     : 'opportunityList'
  }],

  init            : function() {
    this.getOpportunityStore().addListener('load', this.onLoad, this);
    this.control({
      'opportunitylist'                       : {
        render         : this.onRender,
      },
      'opportunityselllist'                   : {
        render         : this.onSellRender,
      },
      'opportunitybuylist'                    : {
        render         : this.onBuyRender,
      },
      'actioncolumn#action-column-opportunity': {
        click          : this.onColumnAction
      },
    });

    this.application.on({
      scope            : this
    });
  },

  onLoad: function() {
    this.getBuyOpportunityStore().load();
    this.getSellOpportunityStore().load();
  },

  onRender: function(list) {
    var column = list.down('[dataIndex=type]');
    var typeStore = this.getOrderTypeStore();
    column.renderer = function(val) {
      var type = typeStore.getAt(val-1);
      return type.data.text;
    };
    column = list.down('[dataIndex=price]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=amount]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=symbol]');
    column.renderer = this.symbolRenderer;
  },

  onSellRender: function(list) {
    var column = list.down('[dataIndex=type]');
    var typeStore = this.getOrderTypeStore();
    column.renderer = function(val) {
      var type = typeStore.getAt(val-1);
      return type.data.text;
    };
    column = list.down('[dataIndex=price]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=symbol]');
    column.renderer = this.symbolRenderer;
  },

  onBuyRender: function(list) {
    column = list.down('[dataIndex=price]');
    column.renderer = this.amountRenderer;
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

      if (rec.get('type') == 1) {
        orderController.openAddOrder(1, null, rec.get('symbol'), rec.get('quantity'), rec.get('price'), rec.get('id'));
      } else {
        orderController.openAddOrder(2, null);
      }
    }
    if (action.indexOf('x-action-col-1') != -1) {
      var str_date = Ext.util.Format.date(rec.get('date'), 'Y-m-d');
      window.open('/charts/' + rec.get('symbol') + '/' + str_date + '.png', '_blank');
    }
    if (action.indexOf('x-action-col-2') != -1) {
      this.getController('Alert').openAddAlert(rec.get('symbol'));
    }
  },

  amountRenderer: function(value, metaData, record) {
    return Ext.util.Format.currency(value);
  },

  symbolRenderer: function(value, metaData, record) {
    return '<a target="_blank" href="http://finance.yahoo.com/q?s='+ value +'">' + value + '</a>';
  },
});
