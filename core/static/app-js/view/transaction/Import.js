Ext.define('semurg.view.transaction.Import', {
    extend: 'Ext.window.Window',
    alias : 'widget.import',

    title : 'Import',
    layout: 'fit',
    autoShow: true,
    modal   : true,
    border  : false,
    width   : 200,

    initComponent: function() {
      this.items = [{
        xtype: 'form',
        border: false,
        url: '/api/import',
        frame: true,
        items: [{
          xtype: 'filefield',
          name : 'importdata',
          allowBlank: false,
          hideLabel: true,
          anchor: '100%',
          emptyText: 'Choose seeesvee ..',
          buttonConfig: {
            iconCls: 'icons-browse'
          },
          buttonText: ''
        }]
      }];

      this.buttons = [{
          text: 'Upload',
          action: 'upload'
        }, {
          text: 'Cancel',
          scope: this,
          handler: this.close
      }];

      this.callParent(arguments);
    }
});
