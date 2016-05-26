Ext.define('semurg.view.transaction.Summary', {
  extend       : 'Ext.Panel',
  alias        : 'widget.summarypanel',

  cls          : 'summary',
  border       : false,
  frame        : false,

  initComponent: function() {
    this.callParent(arguments);
  }
});
