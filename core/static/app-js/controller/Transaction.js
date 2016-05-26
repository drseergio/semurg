Ext.define('semurg.controller.Transaction', {
  extend          : 'Ext.app.Controller',
  views           : [
      'transaction.Add',
      'transaction.Import',
      'transaction.List',
      'transaction.Summary' ],
  stores          : [
      'Order',
      'Position',
      'Transaction',
      'TransactionType' ],
  models          : [ 'Account', 'Transaction' ],

  refs: [{
      selector: 'transactionlist',
      ref     : 'transactionList'
    }, {
      selector: 'transactionadd',
      ref     : 'transactionAdd'
    }, {
      selector: 'summarypanel',
      ref     : 'summaryPanel'
    }, {
      selector: 'import',
      ref     : 'importWindow'
  }],

  init            : function() {
    this.control({
      'transactionlist'                         : {
        render         : this.onRender,
        selectionchange: this.onSelectionChange,
        beforeedit     : this.onBeforeEdit,
        edit           : this.onEdit,
      },
      'summarypanel'                            : {
        render         : this.onSummaryRender
      },
      'transactionlist button[action=deposit]'  : {
        click: function() {
          this.openAddTransaction(4)
        }
      },
      'transactionlist button[action=withdraw]' : {
        click: function() {
          this.openAddTransaction(3)
        }
      },
      'transactionlist button[action=delete]'   : {
        click: this.deleteTransaction
      },
      'transactionlist button[action=import]'   : {
        click: function() {
          this.importData();
        }
      },
      'transactionlist button[action=export]'   : {
        click: this.exportCsv
      },
      'transactionlist button[action=reconcile]': {
        click: this.reconcileTransactions
      },
      'transactionadd textfield[name=amount]'   : {
        afterrender: function(field) {
          field.focus(false, 400);
        }
      },
      'transactionadd button[action=save]'     : {
        click: this.saveTransaction
      },
      'import button[action=upload]': {
        click: function() {
          this.uploadFile();
        }
      },
    });

    this.application.on({
      addtransaction      : this.onAddTransaction,
      deletetransaction   : this.onDeleteTransaction,
      reconciletransaction: this.onReconcileTransaction,
      importtransaction   : this.onImportTransaction,
      scope               : this
    });
  },

  onRender: function(list) {
    var column = list.down('[dataIndex=type]');
    var typeStore = this.getTransactionTypeStore();
    column.renderer = function(val) {
      var type = typeStore.getAt(val-1);
      return type.data.text;
    };
    column = list.down('[dataIndex=amount]');
    column.renderer = this.amountRenderer;
  },

  onSummaryRender: function() {
    var me = this;
    var task = {
      run: function() {
        me.updateSummary();
      },
      interval: 30000
    };
    Ext.TaskManager.start(task);
  },

  onSelectionChange  : function(model, record, index) {
    var win = this.getTransactionList();
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

  onBeforeEdit: function(e) {
    if (e.record.get('reconciled')) {
      return false;
    }
  },

  onEdit: function(e) {
    var orderStore = this.getOrderStore();
    e.store.mySync({
      scope   : this,
      callback: function() {
        orderStore.load();
        this.updateSummary();
      }
    });
  },

  onAddTransaction: function() {
    this.updateSummary();
  },

  onDeleteTransaction: function() {
    this.updateSummary();
  },

  onReconcileTransaction: function() {
    Ext.example.msg(
        'Reconciled',
        'Transactions successfully reconciled');
  },

  onImportTransaction: function() {
    Ext.example.msg(
        'All done',
        'Successfully imported valuable data');

    this.getOrderStore().load();
    this.getPositionStore().load();
    this.getTransactionStore().load();
    this.updateSummary();
  },

  amountRenderer: function(value, metaData, record) {
    var formatted = Ext.util.Format.currency(value, currency);
    if (record.get('type') == 4 || record.get('type') == 2) {
      return '<span style="color:green;">' + formatted + '</span>';
    } else {
      return '<span style="color:red;">' + formatted + '</span>';
    }
  },

  deleteTransaction: function() {
    var list = this.getTransactionList();
    var store = this.getTransactionStore();
    var model = list.getSelectionModel();
    model.selected.each(function(item) {
      store.remove(item);
    });
    var orderStore = this.getOrderStore();
    var positionStore = this.getPositionStore();
    store.mySync({
      scope   : this,
      callback: function() {
        this.application.fireEvent('deletetransaction');
        positionStore.load();
        orderStore.load();
      }
    });
  },

  reconcileTransactions: function() {
    var list = this.getTransactionList();
    var model = list.getSelectionModel();
    var selected = model.getSelection();
    var store = this.getTransactionStore();

    selected.forEach(function(transaction) {
      transaction.set('reconciled', true);
    });

    store.mySync();
    this.application.fireEvent('reconciletransaction');
  },

  openAddTransaction: function(type) {
    var view = Ext.widget('transactionadd');
    var record = Ext.create('semurg.model.Transaction', {
      type: 1,
      date: new Date()
    });
    var form = view.down('form');
    form.loadRecord(record);
    form.down('#combo-transaction-type').setValue(type);
  },

  saveTransaction: function() {
    var win = this.getTransactionAdd();
    var form = win.down('form');
    var values = form.getValues();
    var record = form.getRecord();
    record.set(values);
    var transactionStore = this.getTransactionStore();
    var app = this.application;

    if (form.getForm().isValid()) {
      form.el.mask('Saving..');
      record.save({
        success: function(rec, op) {
          transactionStore.load({
            callback: function() {
              win.close();
              app.fireEvent('addtransaction');
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

  exportCsv: function() {
    var url = 'api/export';
    window.open(url, '_blank');
  },

  updateSummary    : function() {
    var panel = this.getSummaryPanel();
    var me = this;
    var Model = Ext.ModelManager.getModel('semurg.model.Account');
    Model.load(0, {
      success: function(obj) {
        obj.update_summary(panel);
      }
    });
  },

  importData: function() {
    var view = Ext.widget('import');
  },

  uploadFile: function() {
    var win = this.getImportWindow();
    var form = win.down('form');
    var me = this;

    if (form.getForm().isValid()) {
      form.el.mask('Uploading ..');
      form.submit({
        success: function(rec, op) {
          win.close();
          me.commitImport();
        },
        failure: function(rec, op) {
          form.el.unmask();
          var errors = op.result.errors;
          if (errors) {
            form.getForm().markInvalid(errors);
          } else {
            form.down('filefield').markInvalid(op.result.message);
          }
        },
      });
    }
  },

  commitImport: function() {
    var me = this;
    Ext.MessageBox.wait('Actually importing stuff ..');

    setTimeout(function() {
      me.waitProgress(me);
    }, 5000);
  },

  waitProgress: function(me) {
    Ext.Ajax.request({
      method  : 'POST',
      url     : '/api/progress',
      success : function (resp) {
        var result = Ext.decode(resp.responseText);
        if (result.success) {
          me.application.fireEvent('importtransaction');
          Ext.MessageBox.hide();
        } else {
          setTimeout(function() {
            me.waitProgress(me);
          }, 3000);
        }
      },
    });
  }
});
