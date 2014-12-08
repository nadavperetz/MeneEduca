from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views.teachers import DisciplineUpdateView, DisciplineDetailView, AssignmentCreateView

urlpatterns = patterns(
    "",
    url(r"^disciplines/(?P<pk>\d+)/$", DisciplineDetailView.as_view(), name="discipline_detail"),
    url(r"^disciplines/edit/(?P<pk>\d+)/$", DisciplineUpdateView.as_view(), name="discipline_update"),
    url(r"^disciplines/(?P<discipline_id>\d+)/assignments/create/$", AssignmentCreateView.as_view(), name="assignment_create"),
)
