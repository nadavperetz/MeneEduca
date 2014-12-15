from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views.teachers import *

urlpatterns = patterns(
    "",
    url(r"^disciplines/(?P<pk>\d+)/$", DisciplineDetailView.as_view(), name="discipline_detail"),
    url(r"^disciplines/edit/(?P<pk>\d+)/$", DisciplineUpdateView.as_view(), name="discipline_update"),

    url(r"^disciplines/(?P<discipline_id>\d+)/assignments/create/$", AssignmentCreateView.as_view(), name="assignment_create"),
    url(r"^assignments/(?P<pk>\d+)/$", AssignmentDetailView.as_view(), name="assignment_detail"),
    url(r"^assignments/edit/(?P<pk>\d+)/$", AssignmentUpdateView.as_view(), name="assignment_update"),

    url(r"^assignments/(?P<assignment_id>\d+)/groups/$", GroupListView.as_view(), name="group_list"),
    url(r"^groups/(?P<pk>\d+)/$", GroupDetailView.as_view(), name="group_detail"),
    url(r"^groups/edit/(?P<group_id>\d+)/$", "educational.views.teachers.group_update", name="group_update"),
    url(r"^assignments/(?P<assignment_id>\d+)/groups/create/$", "educational.views.teachers.group_create", name="group_create"),
    url(r"^assignments/(?P<assignment_id>\d+)/groups/create_personality/$", "educational.views.teachers.group_create_personality_based", name="group_create_personality_based"),

)
