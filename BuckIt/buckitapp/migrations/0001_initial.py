# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('buckitapp_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_text', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('buckitapp', ['Tag'])

        # Adding model 'Task'
        db.create_table('buckitapp_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task_text', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('buckitapp', ['Task'])

        # Adding M2M table for field tags on 'Task'
        db.create_table('buckitapp_task_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm['buckitapp.task'], null=False)),
            ('tag', models.ForeignKey(orm['buckitapp.tag'], null=False))
        ))
        db.create_unique('buckitapp_task_tags', ['task_id', 'tag_id'])

        # Adding model 'UserProfile'
        db.create_table('buckitapp_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(default=3, max_length=300, null=True)),
        ))
        db.send_create_signal('buckitapp', ['UserProfile'])

        # Adding M2M table for field friends on 'UserProfile'
        db.create_table('buckitapp_userprofile_friends', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_userprofile', models.ForeignKey(orm['buckitapp.userprofile'], null=False)),
            ('to_userprofile', models.ForeignKey(orm['buckitapp.userprofile'], null=False))
        ))
        db.create_unique('buckitapp_userprofile_friends', ['from_userprofile_id', 'to_userprofile_id'])

        # Adding model 'Ownership'
        db.create_table('buckitapp_ownership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userProfile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buckitapp.UserProfile'], null=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buckitapp.Task'], null=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_set', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_done', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('buckitapp', ['Ownership'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('buckitapp_tag')

        # Deleting model 'Task'
        db.delete_table('buckitapp_task')

        # Removing M2M table for field tags on 'Task'
        db.delete_table('buckitapp_task_tags')

        # Deleting model 'UserProfile'
        db.delete_table('buckitapp_userprofile')

        # Removing M2M table for field friends on 'UserProfile'
        db.delete_table('buckitapp_userprofile_friends')

        # Deleting model 'Ownership'
        db.delete_table('buckitapp_ownership')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'buckitapp.ownership': {
            'Meta': {'object_name': 'Ownership'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_done': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_set': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buckitapp.Task']", 'null': 'True'}),
            'userProfile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buckitapp.UserProfile']", 'null': 'True'})
        },
        'buckitapp.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_text': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'buckitapp.task': {
            'Meta': {'object_name': 'Task'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['buckitapp.Tag']", 'symmetrical': 'False'}),
            'task_text': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'buckitapp.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'fb_id': ('django.db.models.fields.CharField', [], {'default': '3', 'max_length': '300', 'null': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'friends_rel_+'", 'null': 'True', 'to': "orm['buckitapp.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['buckitapp.Task']", 'through': "orm['buckitapp.Ownership']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['buckitapp']