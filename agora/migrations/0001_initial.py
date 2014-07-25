# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ForumCategory'
        db.create_table(u'agora_forumcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subcategories', null=True, to=orm['agora.ForumCategory'])),
        ))
        db.send_create_signal(u'agora', ['ForumCategory'])

        # Adding model 'Forum'
        db.create_table(u'agora_forum', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('closed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subforums', null=True, to=orm['agora.Forum'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['agora.ForumCategory'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, on_delete=models.SET_NULL, to=orm['agora.ForumThread'])),
            ('view_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'agora', ['Forum'])

        # Adding M2M table for field groups on 'Forum'
        m2m_table_name = db.shorten_name(u'agora_forum_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('forum', models.ForeignKey(orm[u'agora.forum'], null=False)),
            ('groups', models.ForeignKey(orm[u'profiles.groups'], null=False))
        ))
        db.create_unique(m2m_table_name, ['forum_id', 'groups_id'])

        # Adding model 'ForumThread'
        db.create_table(u'agora_forumthread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'agora_forumthread_related', to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('content_html', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(related_name='threads', to=orm['agora.Forum'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_reply', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['agora.ForumReply'], null=True, on_delete=models.SET_NULL)),
            ('sticky', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('closed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('view_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('reply_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('subscriber_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'agora', ['ForumThread'])

        # Adding model 'ForumReply'
        db.create_table(u'agora_forumreply', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'agora_forumreply_related', to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('content_html', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='replies', to=orm['agora.ForumThread'])),
        ))
        db.send_create_signal(u'agora', ['ForumReply'])

        # Adding model 'UserPostCount'
        db.create_table(u'agora_userpostcount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='post_count', to=orm['auth.User'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'agora', ['UserPostCount'])

        # Adding model 'ThreadSubscription'
        db.create_table(u'agora_threadsubscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscriptions', to=orm['agora.ForumThread'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forum_subscriptions', to=orm['auth.User'])),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal(u'agora', ['ThreadSubscription'])

        # Adding unique constraint on 'ThreadSubscription', fields ['thread', 'user', 'kind']
        db.create_unique(u'agora_threadsubscription', ['thread_id', 'user_id', 'kind'])


    def backwards(self, orm):
        # Removing unique constraint on 'ThreadSubscription', fields ['thread', 'user', 'kind']
        db.delete_unique(u'agora_threadsubscription', ['thread_id', 'user_id', 'kind'])

        # Deleting model 'ForumCategory'
        db.delete_table(u'agora_forumcategory')

        # Deleting model 'Forum'
        db.delete_table(u'agora_forum')

        # Removing M2M table for field groups on 'Forum'
        db.delete_table(db.shorten_name(u'agora_forum_groups'))

        # Deleting model 'ForumThread'
        db.delete_table(u'agora_forumthread')

        # Deleting model 'ForumReply'
        db.delete_table(u'agora_forumreply')

        # Deleting model 'UserPostCount'
        db.delete_table(u'agora_userpostcount')

        # Deleting model 'ThreadSubscription'
        db.delete_table(u'agora_threadsubscription')


    models = {
        u'agora.forum': {
            'Meta': {'object_name': 'Forum'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['agora.ForumCategory']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['profiles.Groups']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['agora.ForumThread']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subforums'", 'null': 'True', 'to': u"orm['agora.Forum']"}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'agora.forumcategory': {
            'Meta': {'object_name': 'ForumCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subcategories'", 'null': 'True', 'to': u"orm['agora.ForumCategory']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'agora.forumreply': {
            'Meta': {'object_name': 'ForumReply'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'agora_forumreply_related'", 'to': u"orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_html': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'to': u"orm['agora.ForumThread']"})
        },
        u'agora.forumthread': {
            'Meta': {'object_name': 'ForumThread'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'agora_forumthread_related'", 'to': u"orm['auth.User']"}),
            'closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_html': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'threads'", 'to': u"orm['agora.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_reply': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['agora.ForumReply']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'reply_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sticky': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subscriber_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'agora.threadsubscription': {
            'Meta': {'unique_together': "[('thread', 'user', 'kind')]", 'object_name': 'ThreadSubscription'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': u"orm['agora.ForumThread']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_subscriptions'", 'to': u"orm['auth.User']"})
        },
        u'agora.userpostcount': {
            'Meta': {'object_name': 'UserPostCount'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_count'", 'to': u"orm['auth.User']"})
        },
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
        u'profiles.groups': {
            'Meta': {'object_name': 'Groups'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['agora']