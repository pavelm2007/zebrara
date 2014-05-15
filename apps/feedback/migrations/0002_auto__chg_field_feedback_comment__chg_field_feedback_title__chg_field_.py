# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Feedback.comment'
        db.alter_column(u'feedback_feedback', 'comment', self.gf('django.db.models.fields.TextField')(default=datetime.datetime(2013, 11, 11, 0, 0)))

        # Changing field 'Feedback.title'
        db.alter_column(u'feedback_feedback', 'title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Feedback.phone'
        db.alter_column(u'feedback_feedback', 'phone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # Changing field 'Feedback.comment'
        db.alter_column(u'feedback_feedback', 'comment', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Feedback.title'
        db.alter_column(u'feedback_feedback', 'title', self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2013, 11, 11, 0, 0), max_length=255))

        # Changing field 'Feedback.phone'
        db.alter_column(u'feedback_feedback', 'phone', self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2013, 11, 11, 0, 0), max_length=255))

    models = {
        u'feedback.feedback': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Feedback'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['feedback']