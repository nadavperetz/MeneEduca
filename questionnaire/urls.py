from django.conf.urls import patterns, url

from .views import QuestionnaireListView, questionnaire_redirect, QuestionnaireDetailView, questionnaire_create_view


urlpatterns = patterns(
    "",
    url(r'^$', QuestionnaireListView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', questionnaire_redirect, name='choice'),
    url(r'^detail/(?P<pk>\d+)/$', QuestionnaireDetailView.as_view(), name='detail'),
    url(r'^answer/(?P<pk>\d+)/$', questionnaire_create_view, name='answer'),
)
