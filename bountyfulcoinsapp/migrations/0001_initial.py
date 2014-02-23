# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Link'
        db.create_table(u'bountyfulcoinsapp_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')
             (unique=True, max_length=200)),
        ))
        db.send_create_signal(u'bountyfulcoinsapp', ['Link'])

        # Adding model 'Bounty'
        db.create_table(u'bountyfulcoinsapp_bounty', (
            (u'id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')
             (max_length=200)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['auth.User'])),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['bountyfulcoinsapp.Link'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')
             (default=0.0, max_digits=20, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')
             (default='BTC', max_length=15)),
        ))
        db.send_create_signal(u'bountyfulcoinsapp', ['Bounty'])

        # Adding model 'Tag'
        db.create_table(u'bountyfulcoinsapp_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')
             (unique=True, max_length=64)),
        ))
        db.send_create_signal(u'bountyfulcoinsapp', ['Tag'])

        # Adding M2M table for field bounties on 'Tag'
        m2m_table_name = db.shorten_name(u'bountyfulcoinsapp_tag_bounties')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(
                orm[u'bountyfulcoinsapp.tag'], null=False)),
            ('bounty', models.ForeignKey(
                orm[u'bountyfulcoinsapp.bounty'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tag_id', 'bounty_id'])

        # Adding model 'SharedBounty'
        db.create_table(u'bountyfulcoinsapp_sharedbounty', (
            (u'id', self.gf('django.db.models.fields.AutoField')
             (primary_key=True)),
            ('bounty', self.gf('django.db.models.fields.related.ForeignKey')
             (to=orm['bountyfulcoinsapp.Bounty'], unique=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')
             (auto_now_add=True, blank=True)),
            ('votes', self.gf(
                'django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'bountyfulcoinsapp', ['SharedBounty'])

        # Adding M2M table for field users_voted on 'SharedBounty'
        m2m_table_name = db.shorten_name(
            u'bountyfulcoinsapp_sharedbounty_users_voted')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(
                verbose_name='ID', primary_key=True, auto_created=True)),
            ('sharedbounty', models.ForeignKey(
                orm[u'bountyfulcoinsapp.sharedbounty'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['sharedbounty_id', 'user_id'])

    def backwards(self, orm):
        # Deleting model 'Link'
        db.delete_table(u'bountyfulcoinsapp_link')

        # Deleting model 'Bounty'
        db.delete_table(u'bountyfulcoinsapp_bounty')

        # Deleting model 'Tag'
        db.delete_table(u'bountyfulcoinsapp_tag')

        # Removing M2M table for field bounties on 'Tag'
        db.delete_table(db.shorten_name(u'bountyfulcoinsapp_tag_bounties'))

        # Deleting model 'SharedBounty'
        db.delete_table(u'bountyfulcoinsapp_sharedbounty')

        # Removing M2M table for field users_voted on 'SharedBounty'
        db.delete_table(
            db.shorten_name(u'bountyfulcoinsapp_sharedbounty_users_voted'))

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
        u'bountyfulcoinsapp.bounty': {
            'Meta': {'object_name': 'Bounty'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '20', 'decimal_places': '2'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'BTC'", 'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bountyfulcoinsapp.Link']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'bountyfulcoinsapp.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'bountyfulcoinsapp.sharedbounty': {
            'Meta': {'object_name': 'SharedBounty'},
            'bounty': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bountyfulcoinsapp.Bounty']", 'unique': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'users_voted': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'bountyfulcoinsapp.tag': {
            'Meta': {'object_name': 'Tag'},
            'bounties': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bountyfulcoinsapp.Bounty']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bountyfulcoinsapp']
