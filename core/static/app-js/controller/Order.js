Ext.define('semurg.controller.Order', {
  extend          : 'Ext.app.Controller',
  views           : [
      'order.Add',
      'order.List' ],
  stores          : [
      'BuyOpportunity',
      'Order',
      'OrderType',
      'Position',
      'SellOpportunity',
      'Transaction' ],
  models          : [ 'Order' ],

  refs: [{
      selector: 'orderlist',
      ref     : 'orderList'
    }, {
      selector: 'orderadd',
      ref     : 'orderAdd'
  }],

  init            : function() {
    this.control({
      'orderlist'                         : {
        render         : this.onRender,
        selectionchange: this.onSelectionChange,
        beforeedit     : this.onBeforeEdit,
        edit           : this.onEdit,
      },
      'orderlist dataview'                : {
        beforedrop     : this.onBeforeDrop,
      },
      'orderlist button[action=buy]'      : {
        click: function() {
          this.openAddOrder(1)
        }
      },
      'orderlist button[action=sell]'     : {
        click: function() {
          this.openAddOrder(2)
        }
      },
      'orderlist button[action=delete]'   : {
        click: this.deleteOrders
      },
      'orderlist button[action=reconcile]': {
        click: this.reconcileOrders
      },
      'orderadd textfield[name=symbol]'   : {
        afterrender: function(field) {
          Ext.defer(this.setFocus, 100, this, [field]);
        }
      },
      'orderadd combo[name=type]'         : {
        select: this.changeType
      },
      'orderadd button[action=save]'      : {
        click: this.saveOrder
      },
      'orderadd #combo-order-type'        : {
        select: this.changeType,
        change: this.changeType
      },
    });

    this.application.on({
      addorder      : this.onAddOrder,
      reconcileorder: this.onReconcileOrder,
      scope         : this
    });
  },

  onRender: function(list) {
    var column = list.down('[dataIndex=type]');
    var typeStore = this.getOrderTypeStore();
    column.renderer = function(val) {
      var type = typeStore.getAt(val-1);
      return type.data.text;
    };
    column = list.down('[dataIndex=fees]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=price]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=total]');
    column.renderer = this.localRenderer;
    column = list.down('[dataIndex=pl]');
    column.renderer = this.deltaRenderer;
    column = list.down('[dataIndex=delta]');
    column.renderer = this.pctRenderer;
    column = list.down('[dataIndex=symbol]');
    column.renderer = this.symbolRenderer;
  },

  onSelectionChange  : function(model, record, index) {
    var win = this.getOrderList();
    var del = win.down('button[action=delete]');
    var reconcile = win.down('button[action=reconcile]');

    if (model.hasSelection()) {
      var reconciled = false;
      model.getSelection().forEach(function(item) {
        if (item.get('reconciled')) {
          reconciled = true;
        }
      });
      if (!reconciled) {
        reconcile.enable();
        del.enable();
      } else {
        reconcile.disable();
        del.disable();
      }
    } else {
      reconcile.disable();
      del.disable();
    }
  },

  onReconcileOrder: function() {
    Ext.example.msg(
        'Reconciled',
        'Orders successfully reconciled');
  },

  onBeforeEdit: function(e) {
    if (e.record.get('reconciled')) {
      return false;
    }
  },

  onEdit: function(e) {
    var transactionStore = this.getTransactionStore();
    e.store.mySync({
      scope   : this,
      callback: function() {
        transactionStore.load();
      }
    });
  },

  onAddOrder: function() {
    this.getTransactionStore().load();
    this.getPositionStore().load();
    this.getSellOpportunityStore().load();
    this.getBuyOpportunityStore().load();
    this.getController('Transaction').updateSummary();
  },

  onBeforeDrop: function(node, data) {
    var rec = data.records[0];
    if (rec.get('type') == 1) {
      this.openAddOrder(1, null, rec.get('symbol'), rec.get('quantity'), rec.get('price'), rec.get('id'));
    } else {
      this.openAddOrder(2, null);
    }
    return false;
  },

  amountRenderer: function(value, metaData, record) {
    return Ext.util.Format.currency(value);
  },

  localRenderer: function(value, metaData, record) {
    return Ext.util.Format.currency(value, currency);
  },

  deltaRenderer: function(value, metaData, record) {
    if (value == 'N/A') {
      return value;
    } else {
      var num = parseFloat(value);
      var formatted = Ext.util.Format.currency(value);
      if (num < 0) {
        return '<span style="color:red;">' + formatted + '</span>';
      } else {
        return '<span style="color:green;">' + formatted + '</span>';
      }
    }
  },

  pctRenderer: function(value, metaData, record) {
    if (value == 'N/A') {
      return value;
    } else {
      var num = parseFloat(value);
      if (num < 0) {
        return '<span style="color:red;">' + num.toFixed(2) + '%</span>';
      } else {
        return '<span style="color:green;">' + num.toFixed(2) + '%</span>';
      }
    }
  },

  setFocus: function(field) {
    var form = field.up('form');
    var combo = form.down('#combo-order-type');
    var comboAccount = form.down('#combo-symbol');
    if (combo.getValue() == 2) {
      comboAccount.focus(false, 400);
    } else {
      field.focus(false, 400);
    }
  },

  deleteOrders: function() {
    var list = this.getOrderList();
    var store = this.getOrderStore();
    var model = list.getSelectionModel();
    model.selected.each(function(item) {
      store.remove(item);
    });
    var transactionStore = this.getTransactionStore();
    var positionStore = this.getPositionStore();

    store.mySync({
      scope   : this,
      callback: function() {
        this.application.fireEvent('deleteorder');
        store.load();
        transactionStore.load();
        positionStore.load();
      }
    });
  },

  reconcileOrders: function() {
    var list = this.getOrderList();
    var model = list.getSelectionModel();
    var selected = model.getSelection();
    var store = this.getOrderStore();

    selected.forEach(function(order) {
      order.set('reconciled', true);
    });

    store.mySync({
      scope   : this,
      callback: function() {
        store.load();
      }
    });

    this.application.fireEvent('reconcileorder');
  },

  openAddOrder: function(type, position, symbol, quantity, price, opportunity) {
    var view = Ext.widget('orderadd');
    var record = Ext.create('semurg.model.Order', {
      type: 1,
      date: new Date()
    });
    if (opportunity) {
      record.set('opportunity', opportunity);
    }
    var form = view.down('form');
    form.loadRecord(record);
    form.down('#combo-order-type').setValue(type);

    if (position != null) {
      form.down('#combo-symbol').setValue(position.get('id'));
    }
    if (quantity != null) {
      form.down('#field-quantity').setValue(quantity);
    }
    if (symbol != null) {
      form.down('#field-symbol').setValue(symbol);
    }
    if (price != null) {
      form.down('#field-price').setValue(price);
    }
  },

  changeType: function(combo, records) {
    var type = combo.getValue();
    var win = this.getOrderAdd();

    if (type == 1) {
      win.down('#field-symbol').show();
      win.down('#combo-symbol').hide();
      win.down('#field-quantity').show();
    } else {
      win.down('#field-symbol').hide();
      win.down('#combo-symbol').show();
      win.down('#field-quantity').hide();
    }
  },

  saveOrder: function() {
    var win = this.getOrderAdd();
    var form = win.down('form');
    var values = form.getValues();
    var record = form.getRecord();
    record.set(values);
    var orderStore = this.getOrderStore();
    var app = this.application;

    if (form.getForm().isValid()) {
      form.el.mask('Saving..');
      record.save({
        success: function(rec, op) {
          orderStore.load({
            callback: function() {
              win.close();
              app.fireEvent('addorder');
            }
          });
        },
        failure: function(rec, op) {
          form.el.unmask();
          var errors = op.request.scope.reader.jsonData['errors'];
          form.getForm().markInvalid(errors);
        },
      });
    }
  },

  symbolRenderer: function(value, metaData, record) {
    return '<a target="_blank" href="http://finance.yahoo.com/q?s='+ value +'">' + value + '</a>';
  },
});
