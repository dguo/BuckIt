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

        # Adding model 'User'
        db.create_table('buckitapp_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('buckitapp', ['User'])

        # Adding M2M table for field friends on 'User'
        db.create_table('buckitapp_user_friends', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_user', models.ForeignKey(orm['buckitapp.user'], null=False)),
            ('to_user', models.ForeignKey(orm['buckitapp.user'], null=False))
        ))
        db.create_unique('buckitapp_user_friends', ['from_user_id', 'to_user_id'])

        # Adding model 'Ownership'
        db.create_table('buckitapp_ownership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buckitapp.User'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['buckitapp.Task'])),
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

        # Deleting model 'User'
        db.delete_table('buckitapp_user')

        # Removing M2M table for field friends on 'User'
        db.delete_table('buckitapp_user_friends')

        # Deleting model 'Ownership'
        db.delete_table('buckitapp_ownership')


    models = {
        'buckitapp.ownership': {
            'Meta': {'object_name': 'Ownership'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_done': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_set': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buckitapp.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['buckitapp.User']"})
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
        'buckitapp.user': {
            'Meta': {'object_name': 'User'},
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'friends_rel_+'", 'null': 'True', 'to': "orm['buckitapp.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['buckitapp.Task']", 'through': "orm['buckitapp.Ownership']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['buckitapp']