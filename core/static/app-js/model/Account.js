Ext.define('semurg.model.Account', {
  extend        : 'Ext.data.Model',
  fields        : [
      'version', 'gullwing_version', 'open', 'date', 'equity', 'cash', 'pct', 'delta' ],

  proxy         : {
    type: 'rest',
    url : '/api/account'
  },

  update_summary: function(panel) {
    var data = {
      'cash': this.get('cash'),
      'version': this.get('version'),
      'gversion': this.get('gullwing_version'),
      'open': this.open(this.get('open')),
      'date': this.get('date'),
      'pct': this.get('pct'),
      'pct_color': this.get_color(this.get('pct')),
      'delta': this.get('delta'),
      'equity': this.get('equity')
    };
    var tpl = Ext.create('Ext.XTemplate',
        '<div class="summary-header">&nbsp;</div>',
        '<div class="summary-inside">',
        'semurg<b>ALPHA</b> [{version}], gullwing [{gversion}], {date}',
        '<div class="summary-amount">',
        '<div class="summary-amount-header">cash</div>',
        '<div class="summary-amount-value">',
        '<span style="font-size: 1.4em;color:black">',
        '{cash:currency("' + currency + '")}</span></div></div>',
        '<div class="summary-amount" style="margin-right: 20px;">',
        '<div class="summary-amount-header">equity</div>',
        '<div class="summary-amount-value">',
        '<span style="font-size: 1.4em;color:black">',
        '{equity:currency}</span></div>',
        '</div>',
        '<div class="summary-amount" style="margin-right: 20px;">',
        '<div class="summary-amount-header">change</div>',
        '<div class="summary-amount-value">',
        '<span style="font-size: 1.4em;color: {pct_color}">',
        '{pct}% ({delta:currency})</span></div>',
        '</div>',
        '<div>',
        '<div style="text-transform: uppercase;">markets are {open}</div></div>',
        '</div>');
    tpl.overwrite(panel.body, data);
  },

  change_sign   : function(val) {
    var fvalue = parseFloat(val);
    return Math.abs(fvalue).toFixed(2);
  },

  open          : function(val) {
    var is_open = parseInt(val);
    if (is_open) {
      return '<span style="color:green;font-size: 1.1em">probably open</span>';
    } else {
      return '<span style="color:red;font-size: 1.1em">closed</span>';
    }
  },

  get_color     : function(val) {
    var fvalue = parseFloat(val);
    if (fvalue < 0) {
      return 'red';
    } else if (fvalue > 0) {
      return 'green';
    } else {
      return 'black';
    }
  }
});
