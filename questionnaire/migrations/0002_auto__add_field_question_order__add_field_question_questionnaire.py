# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field questions on 'Questionnaire'
        db.delete_table(db.shorten_name(u'questionnaire_questionnaire_questions'))

        # Adding field 'Question.order'
        db.add_column(u'questionnaire_question', 'order',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Question.questionnaire'
        db.add_column(u'questionnaire_question', 'questionnaire',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['questionnaire.Questionnaire']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding M2M table for field questions on 'Questionnaire'
        m2m_table_name = db.shorten_name(u'questionnaire_questionnaire_questions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('questionnaire', models.ForeignKey(orm[u'questionnaire.questionnaire'], null=False)),
            ('question', models.ForeignKey(orm[u'questionnaire.question'], null=False))
        ))
        db.create_unique(m2m_table_name, ['questionnaire_id', 'question_id'])

        # Deleting field 'Question.order'
        db.delete_column(u'questionnaire_question', 'order')

        # Deleting field 'Question.questionnaire'
        db.delete_column(u'questionnaire_question', 'questionnaire_id')


    models = {
        u'questionnaire.question': {
            'Meta': {'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.Questionnaire']"}),
            'type_of_answer': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'questionnaire.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['questionnaire']