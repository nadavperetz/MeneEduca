from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin


urlpatterns = patterns('',
                       url(r"^$", "MeneEduca.views.index", name="index"),
                       url(r"^admin/", include(admin.site.urls)),
                       url(r"^account/", include("account.urls", namespace='account')),
                       url(r"^profiles/", include("profiles.urls", namespace='profiles')),
                       url(r"^survey/", include("survey.urls", namespace='survey')),
                       url(r"^forums/", include("agora.urls", namespace='forums'))
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
