from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views.teachers import DisciplineUpdateView, DisciplineDetailView, AssignmentCreateView, AssignmentDetailView
from educational.views.teachers import social_network

urlpatterns = patterns(
    "",
    url(r"^disciplines/(?P<pk>\d+)/$", DisciplineDetailView.as_view(), name="discipline_detail"),
    url(r"^disciplines/edit/(?P<pk>\d+)/$", DisciplineUpdateView.as_view(), name="discipline_update"),
    url(r"^disciplines/(?P<discipline_id>\d+)/assignments/create/$", AssignmentCreateView.as_view(), name="assignment_create"),
    url(r"^assignments/(?P<pk>\d+)/$", AssignmentDetailView.as_view(), name="assignment_detail"),
    url(r"^disciplines/likes/(?P<discipline_id>\d+)/$", social_network, name="social_network"),

)
