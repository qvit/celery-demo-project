# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, handler404, handler500, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

handler404
handler500

urlpatterns = patterns('',
    url(r'^', include('shootr.core.urls')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )