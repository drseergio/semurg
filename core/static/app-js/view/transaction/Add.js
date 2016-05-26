Ext.define('semurg.view.transaction.Add', {
  extend       : 'Ext.window.Window',
  alias        : 'widget.transactionadd',
 
  title        : 'Enter new transaction',
  layout       : 'fit',
  autoShow     : true,
  modal        : true,
  width        : 240,
  closable     : true,

  initComponent: function() {
    this.items = [{
      xtype : 'form',
      frame : true,
      border: false,
      layout: 'anchor',

      items : [{
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype       : 'combo',
              id          : 'combo-transaction-type',
              name        : 'type',
              queryMode   : 'local',
              displayField: 'text',
              valueField  : 'value',
              fieldLabel  : 'Type',
              labelWidth  : 45,
              labelAlign  : 'right',
              anchor      : '100%',
              editable    : false,
              value       : 1,
              store       : 'TransactionType'
          }]
        }, {
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype           : 'datefield',
              fieldLabel      : 'Date',
              labelWidth      : 45,
              labelAlign      : 'right',
              format          : 'Y-m-d',
              allowBlank      : false,
              name            : 'date',
              value           : new Date()
          }]
        }, {
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype           : 'numberfield',
              fieldLabel      : 'Amount',
              labelWidth      : 45,
              labelAlign      : 'right',
              decimalPrecision: 2,
              name            : 'amount',
              anchor          : '100%',
              hideTrigger     : true,
              minValue        : 0.01
          }]
      }]
    }];

    this.buttons = [{
        text   : 'Save',
        action : 'save'
      }, {
        text   : 'Cancel',
        scope  : this,
        handler: this.close
    }];
 
    this.callParent(arguments);
  }
});
