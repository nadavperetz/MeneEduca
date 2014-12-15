from __future__ import unicode_literals

from django.conf.urls import patterns, url
from educational.views.teachers import social_network
import views.teachers
import views.guardians


urlpatterns = patterns(
    "",
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
)
