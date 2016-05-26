Ext.define('semurg.controller.Alert', {
  extend          : 'Ext.app.Controller',
  views           : [
      'alert.Add',
      'alert.List' ],
  stores          : [ 'Alert', 'AlertType' ],
  models          : [ 'Alert' ],

  refs: [{
      selector: 'alertadd',
      ref     : 'alertAdd'
    }, {
      selector: 'alertlist',
      ref     : 'alertList'
  }],

  init            : function() {
    this.control({
      'alertlist'                      : {
        render         : this.onRender,
        selectionchange: this.onSelectionChange,
        edit           : this.onEdit,
      },
      'alertlist button[action=add]'   : {
        click: function() {
          this.openAddAlert();
        }
      },
      'alertlist button[action=delete]': {
        click: this.deleteAlerts
      },
      'alertadd textfield[name=symbol]': {
        afterrender: function(field) {
          Ext.defer(this.setFocus, 100, this, [field]);
        }
      },
      'alertadd button[action=save]'   : {
        click: this.saveAlert
      },
    });

    this.application.on({
      addalert      : this.onAddAlert,
      scope         : this
    });
  },

  onRender: function(list) {
    var column = list.down('[dataIndex=type]');
    var typeStore = this.getAlertTypeStore();
    column.renderer = function(val) {
      var type = typeStore.getAt(val-1);
      return type.data.text;
    };
    column = list.down('[dataIndex=price]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=target]');
    column.renderer = this.amountRenderer;
    column = list.down('[dataIndex=symbol]');
    column.renderer = this.symbolRenderer;
  },

  onAddAlert: function(symbol) {
    Ext.example.msg(
        'Created alert',
        'Successfully created alert');
  },

  onSelectionChange  : function(model, record, index) {
    var win = this.getAlertList();
    var del = win.down('button[action=delete]');

    if (model.hasSelection()) {
      del.enable();
    } else {
      del.disable();
    }
  },

  onEdit: function(e) {
    e.store.mySync();
  },

  amountRenderer: function(value, metaData, record) {
    return Ext.util.Format.currency(value);
  },

  symbolRenderer: function(value, metaData, record) {
    return '<a target="_blank" href="http://finance.yahoo.com/q?s='+ value +'">' + value + '</a>';
  },

  setFocus: function(field) {
    var form = field.up('form');
    field.focus(false, 400);
  },

  openAddAlert: function(symbol) {
    var view = Ext.widget('alertadd');
    var record = Ext.create('semurg.model.Alert', {
      type: 1,
    });
    var form = view.down('form');
    form.loadRecord(record);
    form.down('#combo-alert-type').setValue(1);

    if (symbol != null) {
      form.down('#field-symbol').setValue(symbol);
    }
  },

  saveAlert: function() {
    var win = this.getAlertAdd();
    var form = win.down('form');
    var values = form.getValues();
    var record = form.getRecord();
    record.set(values);
    var alertStore = this.getAlertStore();
    var app = this.application;

    if (form.getForm().isValid()) {
      form.el.mask('Saving..');
      record.save({
        success: function(rec, op) {
          alertStore.load({
            callback: function() {
              win.close();
              app.fireEvent('addalert');
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

  deleteAlerts: function() {
    var list = this.getAlertList();
    var store = this.getAlertStore();
    var model = list.getSelectionModel();
    model.selected.each(function(item) {
      store.remove(item);
    });

    store.mySync({
      scope   : this,
      callback: function() {
        this.application.fireEvent('deletealert');
        store.load();
      }
    });
  },
});
