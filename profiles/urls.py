from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from profiles.views import ProfileEditView


urlpatterns = patterns("",
    url(r"^profile/edit/", login_required(ProfileEditView.as_view()), name="profiles_edit")
)
