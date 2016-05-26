Ext.define('semurg.view.order.Add', {
  extend       : 'Ext.window.Window',
  alias        : 'widget.orderadd',
 
  title        : 'Enter new order',
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
              id          : 'combo-order-type',
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
              store       : 'OrderType'
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
              xtype           : 'textfield',
              id              : 'field-symbol',
              fieldLabel      : 'Symbol',
              labelWidth      : 45,
              labelAlign      : 'right',
              name            : 'symbol',
              anchor          : '100%'
            }, {
              xtype           : 'combo',
              id              : 'combo-symbol',
              displayField    : 'display',
              valueField      : 'id',
              fieldLabel      : 'Symbol',
              labelWidth      : 45,
              labelAlign      : 'right',
              store           : 'Position',
              name            : 'position_id',
              anchor          : '100%',
              hidden          : true,
              editable        : false,
              minChars        : 0
          }]
        }, {
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype           : 'numberfield',
              id              : 'field-price',
              fieldLabel      : 'Price',
              labelWidth      : 45,
              labelAlign      : 'right',
              decimalPrecision: 2,
              name            : 'price',
              anchor          : '100%',
              hideTrigger     : true,
              minValue        : 0.01
          }]
        }, {
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype           : 'numberfield',
              id              : 'field-quantity',
              id              : 'field-quantity',
              fieldLabel      : 'Quantity',
              labelWidth      : 45,
              labelAlign      : 'right',
              decimalPrecision: 0,
              name            : 'quantity',
              anchor          : '100%',
              hideTrigger     : true,
              minValue        : 1
          }]
        }, {
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype           : 'numberfield',
              fieldLabel      : 'Fees',
              labelWidth      : 45,
              labelAlign      : 'right',
              decimalPrecision: 2,
              name            : 'fees',
              anchor          : '100%',
              hideTrigger     : true,
              minValue        : 0
          }]
        }, {
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype           : 'numberfield',
              decimalPrecision: 2,
              fieldLabel      : 'Total',
              labelWidth      : 45,
              labelAlign      : 'right',
              name            : 'total',
              anchor          : '100%',
              hideTrigger     : true,
              minValue        : 0
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
