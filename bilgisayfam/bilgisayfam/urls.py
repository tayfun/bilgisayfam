from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', "entry.views.index_view"),
)
