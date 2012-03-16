# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from shootr.core import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^bundle/(?P<bundle_id>\d+)/', views.get_bundle, name='get_bundle')
)