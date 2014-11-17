# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Section'
        db.create_table(u'main_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Section'])

        # Adding model 'Question'
        db.create_table(u'main_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Section'])),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('question_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Question'])

        # Adding model 'Answer'
        db.create_table(u'main_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Question'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Answer'])


    def backwards(self, orm):
        # Deleting model 'Section'
        db.delete_table(u'main_section')

        # Deleting model 'Question'
        db.delete_table(u'main_question')

        # Deleting model 'Answer'
        db.delete_table(u'main_answer')


    models = {
        u'main.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Question']"})
        },
        u'main.question': {
            'Meta': {'object_name': 'Question'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Section']"})
        },
        u'main.section': {
            'Meta': {'object_name': 'Section'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['main']