# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Survey'
        db.create_table(u'survey_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'survey', ['Survey'])

        # Adding model 'QuestionIpip'
        db.create_table(u'survey_questionipip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Survey'])),
            ('question_number', self.gf('django.db.models.fields.IntegerField')()),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('question_weight', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('answer_value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'survey', ['QuestionIpip'])

        # Adding unique constraint on 'QuestionIpip', fields ['survey', 'question_number']
        db.create_unique(u'survey_questionipip', ['survey_id', 'question_number'])


    def backwards(self, orm):
        # Removing unique constraint on 'QuestionIpip', fields ['survey', 'question_number']
        db.delete_unique(u'survey_questionipip', ['survey_id', 'question_number'])

        # Deleting model 'Survey'
        db.delete_table(u'survey_survey')

        # Deleting model 'QuestionIpip'
        db.delete_table(u'survey_questionipip')


    models = {
        u'survey.questionipip': {
            'Meta': {'unique_together': "(['survey', 'question_number'],)", 'object_name': 'QuestionIpip'},
            'answer_value': ('django.db.models.fields.IntegerField', [], {}),
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