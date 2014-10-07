# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Dialrule', fields ['name']
        db.delete_unique(u'dialrule', ['name'])

        # Removing unique constraint on 'ProviderRule', fields ['name']
        db.delete_unique(u'provider_rule', ['name'])


    def backwards(self, orm):
        # Adding unique constraint on 'ProviderRule', fields ['name']
        db.create_unique(u'provider_rule', ['name'])

        # Adding unique constraint on 'Dialrule', fields ['name']
        db.create_unique(u'dialrule', ['name'])


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
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
            'calls_per_second': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10', 'null': 'True', 'blank': 'True'}),
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
            'password': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'register': ('django.db.models.fields.BooleanField', [], {})
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
            'dayoff': ('django.db.models.fields.BooleanField', [], {}),
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
            'deactive': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lcr': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Lcr']"}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.rate': {
            'Meta': {'object_name': 'Rate', 'db_table': "u'rate'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'increment': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'min_time': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '5'}),
            'rate_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'rates'", 'to': u"orm['core.RateGroup']"}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.RateTag']", 'null': 'True', 'db_table': "u'rategroup_ratetag'", 'blank': 'True'}),
            'tags_string': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'core.rategroup': {
            'Meta': {'object_name': 'RateGroup', 'db_table': "u'rate_group'"},
            'grace_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
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