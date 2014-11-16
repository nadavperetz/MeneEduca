from django.conf.urls import patterns, url

from profiles.views import ProfileEditView


urlpatterns = patterns(
    "",
    url(r"^$", QuestionnaireView.as_view(), name="index")
)
