# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'QuestionIpip.answer_value'
        db.alter_column(u'survey_questionipip', 'answer_value', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'QuestionIpip.answer_value'
        db.alter_column(u'survey_questionipip', 'answer_value', self.gf('django.db.models.fields.IntegerField')(default=0))

    models = {
        u'survey.questionipip': {
            'Meta': {'unique_together': "(['survey', 'question_number'],)", 'object_name': 'QuestionIpip'},
            'answer_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'question_number': ('django.db.models.fields.IntegerField', [], {}),
            'question_weight': ('django.db.models.fields.IntegerField', [], {}),
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