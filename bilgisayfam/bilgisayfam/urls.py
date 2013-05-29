from django.conf.urls import patterns, url
from manifesto.views import ManifestView


urlpatterns = patterns('',
    url(r'^$', "entry.views.index_view"),
    url(r'^manifest\.appcache$', ManifestView.as_view(),
        name="cache_manifest"),
)
