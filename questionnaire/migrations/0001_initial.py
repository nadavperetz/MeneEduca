# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionnaireModel'
        db.create_table(u'questionnaire_questionnairemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'questionnaire', ['QuestionnaireModel'])

        # Adding model 'QuestionModel'
        db.create_table(u'questionnaire_questionmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('type_of_answer', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('weight', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.QuestionnaireModel'])),
        ))
        db.send_create_signal(u'questionnaire', ['QuestionModel'])

        # Adding model 'QuestionAnswered'
        db.create_table(u'questionnaire_questionanswered', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.QuestionModel'])),
        ))
        db.send_create_signal(u'questionnaire', ['QuestionAnswered'])

        # Adding model 'QuestionnaireAnswered'
        db.create_table(u'questionnaire_questionnaireanswered', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.QuestionnaireModel'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Student'])),
        ))
        db.send_create_signal(u'questionnaire', ['QuestionnaireAnswered'])

        # Adding M2M table for field answers on 'QuestionnaireAnswered'
        m2m_table_name = db.shorten_name(u'questionnaire_questionnaireanswered_answers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('questionnaireanswered', models.ForeignKey(orm[u'questionnaire.questionnaireanswered'], null=False)),
            ('questionanswered', models.ForeignKey(orm[u'questionnaire.questionanswered'], null=False))
        ))
        db.create_unique(m2m_table_name, ['questionnaireanswered_id', 'questionanswered_id'])


    def backwards(self, orm):
        # Deleting model 'QuestionnaireModel'
        db.delete_table(u'questionnaire_questionnairemodel')

        # Deleting model 'QuestionModel'
        db.delete_table(u'questionnaire_questionmodel')

        # Deleting model 'QuestionAnswered'
        db.delete_table(u'questionnaire_questionanswered')

        # Deleting model 'QuestionnaireAnswered'
        db.delete_table(u'questionnaire_questionnaireanswered')

        # Removing M2M table for field answers on 'QuestionnaireAnswered'
        db.delete_table(db.shorten_name(u'questionnaire_questionnaireanswered_answers'))


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'complete_profile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'profiles.student': {
            'Meta': {'object_name': 'Student'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['profiles.Profile']", 'unique': 'True'})
        },
        u'questionnaire.questionanswered': {
            'Meta': {'object_name': 'QuestionAnswered'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.QuestionModel']"})
        },
        u'questionnaire.questionmodel': {
            'Meta': {'object_name': 'QuestionModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.QuestionnaireModel']"}),
            'type_of_answer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'questionnaire.questionnaireanswered': {
            'Meta': {'object_name': 'QuestionnaireAnswered'},
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['questionnaire.QuestionAnswered']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.QuestionnaireModel']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.Student']"})
        },
        u'questionnaire.questionnairemodel': {
            'Meta': {'object_name': 'QuestionnaireModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['questionnaire']