from django.conf.urls import patterns, url


urlpatterns = patterns(
    "survey.views",
    #url(r"^$", "forums", name="agora_forums"),
    url(r"^$", "index", name="index"),
    url(r"^survey/(?P<survey_id>\d+)/$", "survey_ipip", name="survey_ipip"),
    url(r"^survey/results/(?P<survey_id>\d+)/$", "survey_result", name="survey_result"),
)
