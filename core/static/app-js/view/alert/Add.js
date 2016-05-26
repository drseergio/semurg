Ext.define('semurg.view.alert.Add', {
  extend       : 'Ext.window.Window',
  alias        : 'widget.alertadd',
 
  title        : 'Create new alert',
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
              xtype           : 'textfield',
              id              : 'field-symbol',
              fieldLabel      : 'Symbol',
              labelWidth      : 45,
              labelAlign      : 'right',
              name            : 'symbol',
              anchor          : '100%'
          }]
        }, {
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype       : 'combo',
              id          : 'combo-alert-type',
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
              store       : 'AlertType'
          }]
        }, {
          xtype : 'container',
          layout: 'column',
          items : [{
              xtype           : 'numberfield',
              id              : 'field-price',
              fieldLabel      : 'Target',
              labelWidth      : 45,
              labelAlign      : 'right',
              decimalPrecision: 2,
              name            : 'target',
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
