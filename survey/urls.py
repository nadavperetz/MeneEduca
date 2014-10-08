from __future__ import unicode_literals

from django.conf.urls import patterns, url
from .views import SurveyListView, SurveyCompletedListView


urlpatterns = patterns(
    "survey.views",
    url(r"^$", SurveyListView.as_view(), name="index"),
    url(r"^completed/$", SurveyCompletedListView.as_view(), name="completed"),
    url(r"sent/(?P<slug>.*)/$", "form_sent", name="form_sent"),
    url(r"detail/(?P<slug>.*)/$", "form_detail", name="form_detail"),
)
