Ext.Loader.setPath('Ext.ux', staticPath + 'js-extra');
Ext.require([
  'Ext.chart.*',
  'Ext.form.*',
  'Ext.dd.*',
  'Ext.util.Cookies',
  'Ext.Ajax',
  'Ext.data.writer.Json',
  'Ext.data.Store',
  'Ext.data.TreeStore',
  'Ext.resizer.*',
  'Ext.layout.*',
  'Ext.grid.*',
  'Ext.tree.*',
  'Ext.state.*',
  'Ext.tab.*',
  'Ext.ux.CheckColumn',
  'Ext.selection.*'], function() {
    Ext.override(Ext.selection.RowModel, {
      onRowMouseDown: function (view, record, item, index, e) {
        if (!this.allowRightMouseSelection(e)) {
          return;
        }
        this.selectWithEvent(record, e);
      }
    });

    Ext.override(Ext.grid.plugin.CellEditing, {
      onEditComplete : function(ed, value, startValue) {
        var me = this,
          grid = me.grid,
          sm = grid.getSelectionModel(),
          activeColumn = me.getActiveColumn(),
          dataIndex;

        if (activeColumn) {
          dataIndex = activeColumn.dataIndex;

          me.setActiveEditor(null);
          me.setActiveColumn(null);
          me.setActiveRecord(null);
          delete sm.wasEditing;

          if (!me.validateEdit()) {
            return;
          }
          if (value !== startValue) {
            me.context.record.set(dataIndex, value);
          }
          me.context.value = value;
          me.fireEvent('edit', me, me.context);
        }
      }
    });

    Ext.override(Ext.grid.Scroller, {
      afterRender: function() {
        var me = this;
        me.callParent();
        me.mon(me.scrollEl, 'scroll', me.onElScroll, me);
        Ext.cache[me.el.id].skipGarbageCollection = true;
        Ext.EventManager.addListener(me.scrollEl, 'scroll', me.onElScrollCheck, me);
        Ext.cache[me.scrollEl.id].skipGarbageCollection = true;
      },

      wasScrolled: false,

      onElScroll: function(event, target) {
        this.wasScrolled = true;
        this.fireEvent('bodyscroll', event, target);
      },

      onElScrollCheck: function(event, target, options) {
        var me = this;

        if (!me.wasScrolled) {
          me.mon(me.scrollEl, 'scroll', me.onElScroll, me);
        }
        me.wasScrolled = false;
      }
    });

    Ext.data.writer.Json.override({
      getRecordData: function(record) {
        var me = this, i, association, childStore, data = {}, fields = record.fields;
        if (record.proxy.writer.writeAllFields) {
          data = record.data;

          fields.each(function(field) {
            if (field.persist) {
              name = field[nameProperty] || field.name;
              data[name] = record.get(field.name);
              if (field.dateFormat && Ext.isDate(data[name])) {
                data[name] = Ext.Date.format(data[name], field.dateFormat);
              }
            }
          });
        } else {
          var changes, name,  field, fields = record.fields, nameProperty = this.nameProperty, key;
          changes = record.getChanges();
          for (key in changes) {
            if (changes.hasOwnProperty(key)) {
              field = fields.get(key);
              name = field[nameProperty] || field.name;
              if (field.dateFormat && Ext.isDate(changes[key])) {
                data[name] = Ext.Date.format(changes[key], field.dateFormat);
              } else {
                data[name] = changes[key];
              }
            }
          }
          if (!record.phantom) {
            data[record.idProperty] = record.getId();
          }
        }

        for (i = 0; i < record.associations.length; i++) {
          association = record.associations.get(i);
          if (association.type != 'hasMany') {
            continue;
          }
          data[association.name] = [];
          childStore = record[association.storeName];

          if (!childStore) continue;

          childStore.each(function(childRecord) {
            var childData = this.getRecordData.call(this, childRecord);

            if (childRecord.dirty | childRecord.phantom | (childData != null)) {
              data[association.name].push(childData);
              record.setDirty();
            }
          }, me);

          Ext.each(childStore.removed, function(removedChildRecord) {
            removedChildRecord.set('forDeletion', true);
            var removedChildData = this.getRecordData.call(this, removedChildRecord);
            data[association.name].push(removedChildData);
            record.setDirty();
          }, me);
        }

        if (record.dirty | record.phantom | record.get('forDeletion')){
            return data;
        }
      }
    });

    Ext.data.Store.override({
      mySync: function(options) {
        if (Ext.isObject(options)) {
          this.on("write", function(store, operation) {
            if (Ext.isDefined(options.scope)) {
              options.callback.call(options.scope);
            } else {
              options.callback.call(this);
            }
            store.un("write", options.callback);
          });
        }

        this.sync();
      },

      remove: function(records, /* private */ isMove) {
        if (!Ext.isArray(records)) {
          records = [records];
        }

        isMove = isMove === true;
        var me = this,
          sync = false,
          i = 0,
          length = records.length,
          isPhantom,
          index,
          record;

        for (; i < length; i++) {
            record = records[i];
            index = me.data.indexOf(record);

            if (me.snapshot) {
              me.snapshot.remove(record);
            }

            if (index > -1) {
              isPhantom = record.phantom === true;
              if (!isMove && !isPhantom) {
                record.set('forDeletion', true);
                me.removed.push(record);
              }

              record.unjoin(me);
              me.data.remove(record);
              sync = sync || !isPhantom;
              me.fireEvent('remove', me, record, index);
            }
        }

        me.fireEvent('datachanged', me);
        if (!isMove && me.autoSync && sync) {
          me.sync();
        }
      }
    });

    Ext.application({
      name       : 'semurg',
      appFolder  : staticPath + 'app-js',
      controllers: controllers,

      launch     : function() {
        Ext.apply(Ext.form.field.VTypes, {
          year: function(val, field) {
          return /^\d{4}$/.test(val);
        },
        yearText: 'Not a valid year. Must be in the format "2010".',
        yearMask: /[\d]/i
      });

      Ext.example = function(){
        var msgCt;

        function createBox(t, s) {
          return '<div class="msg"><h3>' + t + '</h3><p>' + s + '</p></div>';
        }
        return {
            msg : function(title, format) {
              if (!msgCt){
                msgCt = Ext.core.DomHelper.insertFirst(document.body, {id:'msg-div'}, true);
              }
              var s = Ext.String.format.apply(String, Array.prototype.slice.call(arguments, 1));
              var m = Ext.core.DomHelper.append(msgCt, createBox(title, s), true);
              m.hide();
              m.slideIn('t').ghost("t", { delay: 1000, remove: true});
            },
            init : function(){
            }
        };
      }();

      startSemurg();
    }
  });
});
