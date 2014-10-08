from __future__ import unicode_literals

from django.conf.urls import patterns, url
from .views import SurveyListView


urlpatterns = patterns(
    "survey.views",
    url(r"^$", SurveyListView.as_view(), name="index"),
    url(r"(?P<slug>.*)/sent/$", "form_sent", name="form_sent"),
    url(r"(?P<slug>.*)/$", "form_detail", name="form_detail"),
)
