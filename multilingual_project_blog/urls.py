"""URLs for the ``multilingual_project_blog`` app."""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from cms.sitemaps import CMSSitemap
from django_libs.views import RapidPrototypingView
from multilingual_news.sitemaps import NewsSitemap

from .feeds import CustomNewsEntriesFeed


admin.autodiscover()


urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

if settings.ENVIRONMENT == 'dev':
    urlpatterns += patterns(
        '',
        url(r'^rosetta/', include('rosetta.urls')),
    )

urlpatterns += patterns(
    '',
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {
        'sitemaps': {
            'cmspages': CMSSitemap,
            'blogentries': NewsSitemap,
        }, }),
    url(r'^hero-slider/', include('hero_slider.urls')),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        name='auth_login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^prototype/(?P<template_path>.*)$',
        RapidPrototypingView.as_view(),
        name='prototype'),
    url(r'^ics-generator/', include('ics_generator.urls')),
    url(r'^blog/rss/any/$', CustomNewsEntriesFeed(), {'any_language': True},
        name='news_rss_any'),
    url(r'^pos/', include('generic_positions.urls')),
    url(r'^', include('cms.urls')),
)
