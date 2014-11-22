from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views.teachers import DisciplineUpdateView, DisciplineDetailView


urlpatterns = patterns(
    "",
    url(r"^discipline/(?P<pk>\d+)/$", DisciplineDetailView.as_view(), name="discipline_detail"),
    url(r"^discipline/edit/(?P<pk>\d+)/$", DisciplineUpdateView.as_view(), name="discipline_update"),

)
