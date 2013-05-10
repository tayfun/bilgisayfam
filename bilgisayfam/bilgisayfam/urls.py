from django.conf.urls import patterns, include, url

import qhonuskan_votes.urls
# from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# from entry.views import index_view

urlpatterns = patterns('',
    # url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^$', "entry.views.index_view"),
    url(r'^votes/', include(qhonuskan_votes.urls)),

    # Examples:
    # url(r'^$', 'bilgisayfam.views.home', name='home'),
    # url(r'^bilgisayfam/', include('bilgisayfam.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
