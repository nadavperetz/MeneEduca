# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table(u'questionnaire_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('type_of_answer', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'questionnaire', ['Question'])

        # Adding model 'Questionnaire'
        db.create_table(u'questionnaire_questionnaire', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'questionnaire', ['Questionnaire'])

        # Adding M2M table for field questions on 'Questionnaire'
        m2m_table_name = db.shorten_name(u'questionnaire_questionnaire_questions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('questionnaire', models.ForeignKey(orm[u'questionnaire.questionnaire'], null=False)),
            ('question', models.ForeignKey(orm[u'questionnaire.question'], null=False))
        ))
        db.create_unique(m2m_table_name, ['questionnaire_id', 'question_id'])


    def backwards(self, orm):
        # Deleting model 'Question'
        db.delete_table(u'questionnaire_question')

        # Deleting model 'Questionnaire'
        db.delete_table(u'questionnaire_questionnaire')

        # Removing M2M table for field questions on 'Questionnaire'
        db.delete_table(db.shorten_name(u'questionnaire_questionnaire_questions'))


    models = {
        u'questionnaire.question': {
            'Meta': {'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type_of_answer': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'questionnaire.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['questionnaire.Question']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['questionnaire']