# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'QuestionIpip.question_weight'
        db.alter_column(u'survey_questionipip', 'question_weight', self.gf('django.db.models.fields.CharField')(max_length=1))

    def backwards(self, orm):

        # Changing field 'QuestionIpip.question_weight'
        db.alter_column(u'survey_questionipip', 'question_weight', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'survey.questionipip': {
            'Meta': {'unique_together': "(['survey', 'question_number'],)", 'object_name': 'QuestionIpip'},
            'answer_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'question_number': ('django.db.models.fields.IntegerField', [], {}),
            'question_weight': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Survey']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'survey.survey': {
            'Meta': {'object_name': 'Survey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['survey']