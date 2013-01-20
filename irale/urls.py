from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^id/(\d+)/$', 'pfinder.views.lookupId'),
    url(r'^search/(\w+)/$', 'pfinder.views.lookupKey'),
    url(r'^search/(?P<key>\w+)/(?P<value>\w+)/$', 'pfinder.views.lookupToken'),
    url(r'^bounds/$', 'pfinder.views.lookupBounds'),
    url(r'^around/$', 'pfinder.views.lookupAround'),
    url(r'^new/$', 'pfinder.views.createNew'),
    url(r'^edit/(\d+)/$', 'pfinder.views.editId'),
    url(r'^attach/(\d+)/$', 'pfinder.views.addToken'),
    url(r'^admin/', include(admin.site.urls)),
)
