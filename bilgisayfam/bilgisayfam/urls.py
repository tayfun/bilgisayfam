from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from manifesto.views import ManifestView


urlpatterns = patterns('',
    url(r'^$', "entry.views.index_view"),
    url(r'^manifest\.appcache$', cache_page(60 * 15)(ManifestView.as_view()),
        name="cache_manifest"),
)
