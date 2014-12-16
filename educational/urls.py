from __future__ import unicode_literals

from django.conf.urls import patterns, url

import views.teachers
import views.guardians
from .views.teachers import DisciplineDetailView, AssignmentCreateView, AssignmentDetailView
from educational.views.teachers import social_network, RemainderCreateView

urlpatterns = patterns(
    "",
    url(r"^disciplines/create/$", 'educational.views.teachers.discipline_create', name="discipline_create"),
    url(r"^disciplines/(?P<pk>\d+)/$", DisciplineDetailView.as_view(), name="discipline_detail"),
    url(r"^disciplines/edit/(?P<pk>\d+)/$", 'educational.views.teachers.discipline_update', name="discipline_update"),
    url(r"^disciplines/(?P<discipline_id>\d+)/assignments/create/$", AssignmentCreateView.as_view(), name="assignment_create"),
    url(r"^assignments/(?P<pk>\d+)/$", AssignmentDetailView.as_view(), name="assignment_detail"),
    url(r"^disciplines/(?P<discipline_id>\d+)/assignments/create/$", views.teachers.AssignmentCreateView.as_view(), name="assignment_create"),
    url(r"^assignments/(?P<pk>\d+)/$", views.teachers.AssignmentDetailView.as_view(), name="assignment_detail"),
    url(r"^assignments/edit/(?P<pk>\d+)/$", views.teachers.AssignmentUpdateView.as_view(), name="assignment_update"),

    url(r"^assignments/(?P<assignment_id>\d+)/groups/$", views.teachers.GroupListView.as_view(), name="group_list"),
    url(r"^groups/(?P<pk>\d+)/$", views.teachers.GroupDetailView.as_view(), name="group_detail"),
    url(r"^groups/edit/(?P<group_id>\d+)/$", "educational.views.teachers.group_update", name="group_update"),
    url(r"^assignments/(?P<assignment_id>\d+)/groups/create/$", "educational.views.teachers.group_create", name="group_create"),
    url(r"^assignments/(?P<assignment_id>\d+)/groups/create_personality/$", "educational.views.teachers.group_create_personality_based", name="group_create_personality_based"),

    url(r"^guardians/assignments/(?P<pk>\d+)/$", views.guardians.AssignmentDetailView.as_view(), name="assignment_detail_guardian"),
    url(r"^disciplines/likes/(?P<discipline_id>\d+)/$", social_network, name="social_network"),

    url(r"^remainders/create/(?P<discipline_id>\d+)/$", RemainderCreateView.as_view(), name="remainder_create")
)
