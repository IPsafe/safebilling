# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from ipsafe.settings import PROJECT_ROOT

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table(u'customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('web_site', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('devices_limit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('activecalls_limit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('calls_per_second', self.gf('django.db.models.fields.PositiveIntegerField')(default=10)),
            ('customer_balance', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=12, decimal_places=6)),
            ('postpaid_limit', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('lcr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Lcr'])),
            ('rate_groups', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.RateGroup'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Customer'])

        # Adding model 'Blacklist'
        db.create_table(u'blacklist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('did', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'core', ['Blacklist'])

        # Adding model 'Codec'
        db.create_table(u'codec', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codec', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'core', ['Codec'])

        # Adding model 'Device'
        db.create_table(u'device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Customer'])),
            ('dialrules_groups', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.DialruleGroup'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('device_type', self.gf('django.db.models.fields.CharField')(default=u'extension', max_length=20, blank=True)),
            ('accountcode', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('callerid', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('context', self.gf('django.db.models.fields.CharField')(default=u'default', max_length=80, null=True, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=31, null=True, blank=True)),
            ('port', self.gf('django.db.models.fields.CharField')(default=u'5060', max_length=5, null=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('codec_inbound', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('codec_outbound', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('codec_inbound_string', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('codec_outbound_string', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'core', ['Device'])

        # Adding model 'ProviderRule'
        db.create_table(u'provider_rule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gateway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Gateway'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('cut', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('add', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('min_len', self.gf('django.db.models.fields.IntegerField')()),
            ('max_len', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['ProviderRule'])

        # Adding model 'Gateway'
        db.create_table(u'gateway', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Provider'])),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('register', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accountcode', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('callerid', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('fromuser', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('fromdomain', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=31, null=True, blank=True)),
            ('permit', self.gf('django.db.models.fields.CharField')(max_length=95, blank=True)),
            ('deny', self.gf('django.db.models.fields.CharField')(max_length=95, blank=True)),
            ('port', self.gf('django.db.models.fields.CharField')(default=u'5060', max_length=5, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('codec_inbound', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('codec_outbound', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('codec_inbound_string', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('codec_outbound_string', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('activecalls_limit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('calls_per_second', self.gf('django.db.models.fields.PositiveIntegerField')(default=10)),
        ))
        db.send_create_signal(u'core', ['Gateway'])

        # Adding model 'Provider'
        db.create_table(u'provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('web_site', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('postpaid_limit', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('context', self.gf('django.db.models.fields.CharField')(default=u'provider', max_length=80, blank=True)),
            ('rate_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.RateGroup'])),
        ))
        db.send_create_signal(u'core', ['Provider'])

        # Adding model 'Dialrule'
        db.create_table(u'dialrule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dialrule_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.DialruleGroup'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('cut', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('add', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('min_len', self.gf('django.db.models.fields.IntegerField')()),
            ('max_len', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['Dialrule'])

        # Adding model 'DialruleGroup'
        db.create_table(u'dialrule_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'core', ['DialruleGroup'])

        # Adding model 'InboundRoute'
        db.create_table(u'inbound_route', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Provider'])),
            ('area_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('did', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
        ))
        db.send_create_signal(u'core', ['InboundRoute'])

        # Adding model 'InboundRule'
        db.create_table(u'inbound_rule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inbound_route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.InboundRoute'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('destination', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('weekdays', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('start', self.gf('django.db.models.fields.TimeField')(default=u'00:00:00')),
            ('stop', self.gf('django.db.models.fields.TimeField')(default=u'23:59:59')),
            ('dayoff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('specific_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['InboundRule'])

        # Adding model 'Lcr'
        db.create_table(u'lcr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('order', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'core', ['Lcr'])

        # Adding model 'LcrProvider'
        db.create_table(u'lcr_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lcr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Lcr'])),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Provider'])),
            ('deactive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'core', ['LcrProvider'])

        # Adding model 'RateTag'
        db.create_table(u'rate_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
        ))
        db.send_create_signal(u'core', ['RateTag'])

        # Adding model 'Rate'
        db.create_table(u'rate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rate_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'rates', to=orm['core.RateGroup'])),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=10, decimal_places=2)),
            ('min_time', self.gf('django.db.models.fields.IntegerField')(default=1, null=True)),
            ('increment', self.gf('django.db.models.fields.IntegerField')(default=1, null=True)),
        ))
        db.send_create_signal(u'core', ['Rate'])

        # Adding model 'RateGroup'
        db.create_table(u'rate_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
        ))
        db.send_create_signal(u'core', ['RateGroup'])

        # Adding model 'Cdr'
        db.create_table(u'cdr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Customer'])),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('uuid_b', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('accountcode', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('caller_id', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Device'])),
            ('destination_number', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('lcr_name', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('rate_group', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('billsec', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Provider'], null=True, blank=True)),
            ('gateway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Gateway'], null=True, blank=True)),
            ('hangup_cause', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('hangup_cause_q850', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('remote_media_ip', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('endpoint_disposition', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('hangup_disposition', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('read_codec', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('write_codec', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('cdr_object_id', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('user_billsec', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('provider_billsec', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('provider_cost', self.gf('django.db.models.fields.DecimalField')(default=u'0', null=True, max_digits=11, decimal_places=5)),
            ('user_cost', self.gf('django.db.models.fields.DecimalField')(default=u'0', null=True, max_digits=11, decimal_places=5)),
            ('provider_rate_name', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('provider_rate_prefix', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('provider_rate_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('provider_rate_min_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('provider_rate_increment', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('provider_rate_tags', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('user_rate_name', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('user_rate_prefix', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('user_rate_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('user_rate_min_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('user_rate_increment', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('user_rate_tags', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('progressmedia_time', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Cdr'])

        for line in file(PROJECT_ROOT + '/core/sql/codec.sql').readlines():
            db.execute(line)

        for line in file(PROJECT_ROOT + '/core/sql/ratetag.sql').readlines():
            db.execute(line)


    def backwards(self, orm):
        # Deleting model 'Customer'
        db.delete_table(u'customer')

        # Deleting model 'Blacklist'
        db.delete_table(u'blacklist')

        # Deleting model 'Codec'
        db.delete_table(u'codec')

        # Deleting model 'Device'
        db.delete_table(u'device')

        # Deleting model 'ProviderRule'
        db.delete_table(u'provider_rule')

        # Deleting model 'Gateway'
        db.delete_table(u'gateway')

        # Deleting model 'Provider'
        db.delete_table(u'provider')

        # Deleting model 'Dialrule'
        db.delete_table(u'dialrule')

        # Deleting model 'DialruleGroup'
        db.delete_table(u'dialrule_group')

        # Deleting model 'InboundRoute'
        db.delete_table(u'inbound_route')

        # Deleting model 'InboundRule'
        db.delete_table(u'inbound_rule')

        # Deleting model 'Lcr'
        db.delete_table(u'lcr')

        # Deleting model 'LcrProvider'
        db.delete_table(u'lcr_provider')

        # Deleting model 'RateTag'
        db.delete_table(u'rate_tag')

        # Deleting model 'Rate'
        db.delete_table(u'rate')

        # Deleting model 'RateGroup'
        db.delete_table(u'rate_group')

        # Deleting model 'Cdr'
        db.delete_table(u'cdr')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.blacklist': {
            'Meta': {'object_name': 'Blacklist', 'db_table': "u'blacklist'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'did': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.cdr': {
            'Meta': {'object_name': 'Cdr', 'db_table': "u'cdr'"},
            'accountcode': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'billsec': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'caller_id': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'cdr_object_id': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Customer']"}),
            'destination_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Device']"}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'endpoint_disposition': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'gateway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Gateway']", 'null': 'True', 'blank': 'True'}),
            'hangup_cause': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'hangup_cause_q850': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'hangup_disposition': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lcr_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'progressmedia_time': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Provider']", 'null': 'True', 'blank': 'True'}),
            'provider_billsec': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'provider_cost': ('django.db.models.fields.DecimalField', [], {'default': "u'0'", 'null': 'True', 'max_digits': '11', 'decimal_places': '5'}),
            'provider_rate_increment': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'provider_rate_min_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'provider_rate_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'provider_rate_prefix': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'provider_rate_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'provider_rate_tags': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rate_group': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'read_codec': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'remote_media_ip': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user_billsec': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'user_cost': ('django.db.models.fields.DecimalField', [], {'default': "u'0'", 'null': 'True', 'max_digits': '11', 'decimal_places': '5'}),
            'user_rate_increment': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'user_rate_min_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'user_rate_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'user_rate_prefix': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user_rate_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'user_rate_tags': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'uuid_b': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'write_codec': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'})
        },
        u'core.codec': {
            'Meta': {'object_name': 'Codec', 'db_table': "u'codec'"},
            'codec': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.customer': {
            'Meta': {'object_name': 'Customer', 'db_table': "u'customer'"},
            'activecalls_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'calls_per_second': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'customer_balance': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '12', 'decimal_places': '6'}),
            'devices_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lcr': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Lcr']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'postpaid_limit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'rate_groups': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.RateGroup']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'web_site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'core.device': {
            'Meta': {'object_name': 'Device', 'db_table': "u'device'"},
            'accountcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'callerid': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'codec_inbound': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'codec_inbound_string': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'codec_outbound': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'codec_outbound_string': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'context': ('django.db.models.fields.CharField', [], {'default': "u'default'", 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Customer']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'device_type': ('django.db.models.fields.CharField', [], {'default': "u'extension'", 'max_length': '20', 'blank': 'True'}),
            'dialrules_groups': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DialruleGroup']", 'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'port': ('django.db.models.fields.CharField', [], {'default': "u'5060'", 'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        u'core.dialrule': {
            'Meta': {'object_name': 'Dialrule', 'db_table': "u'dialrule'"},
            'add': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'cut': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dialrule_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DialruleGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_len': ('django.db.models.fields.IntegerField', [], {}),
            'min_len': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.dialrulegroup': {
            'Meta': {'object_name': 'DialruleGroup', 'db_table': "u'dialrule_group'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.gateway': {
            'Meta': {'object_name': 'Gateway', 'db_table': "u'gateway'"},
            'accountcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'activecalls_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'callerid': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'calls_per_second': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'codec_inbound': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'codec_inbound_string': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'codec_outbound': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'codec_outbound_string': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'deny': ('django.db.models.fields.CharField', [], {'max_length': '95', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'fromdomain': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'fromuser': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '31', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'permit': ('django.db.models.fields.CharField', [], {'max_length': '95', 'blank': 'True'}),
            'port': ('django.db.models.fields.CharField', [], {'default': "u'5060'", 'max_length': '5', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Provider']"}),
            'register': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'core.inboundroute': {
            'Meta': {'object_name': 'InboundRoute', 'db_table': "u'inbound_route'"},
            'area_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'did': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Provider']"})
        },
        u'core.inboundrule': {
            'Meta': {'object_name': 'InboundRule', 'db_table': "u'inbound_rule'"},
            'dayoff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'destination': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbound_route': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.InboundRoute']"}),
            'specific_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {'default': "u'00:00:00'"}),
            'stop': ('django.db.models.fields.TimeField', [], {'default': "u'23:59:59'"}),
            'weekdays': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        u'core.lcr': {
            'Meta': {'object_name': 'Lcr', 'db_table': "u'lcr'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'core.lcrprovider': {
            'Meta': {'ordering': "(u'priority',)", 'object_name': 'LcrProvider', 'db_table': "u'lcr_provider'"},
            'deactive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lcr': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Lcr']"}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Provider']"})
        },
        u'core.provider': {
            'Meta': {'object_name': 'Provider', 'db_table': "u'provider'"},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'context': ('django.db.models.fields.CharField', [], {'default': "u'provider'", 'max_length': '80', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'postpaid_limit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'rate_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.RateGroup']"}),
            'web_site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'core.providerrule': {
            'Meta': {'object_name': 'ProviderRule', 'db_table': "u'provider_rule'"},
            'add': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'cut': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'gateway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Gateway']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_len': ('django.db.models.fields.IntegerField', [], {}),
            'min_len': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.rate': {
            'Meta': {'object_name': 'Rate', 'db_table': "u'rate'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'increment': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'min_time': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'rate_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'rates'", 'to': u"orm['core.RateGroup']"}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'core.rategroup': {
            'Meta': {'object_name': 'RateGroup', 'db_table': "u'rate_group'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        u'core.ratetag': {
            'Meta': {'object_name': 'RateTag', 'db_table': "u'rate_tag'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'})
        }
    }

    complete_apps = ['core']