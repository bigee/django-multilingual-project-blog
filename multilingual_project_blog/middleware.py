"""Middlewares for the ``multilingual_project_blog`` app."""
import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation


class CanonicalURLMiddleware(object):
    """
    Redirects to /pl /en /de etc. if no language is found in the URL.

    """
    def process_request(self, request):
        if request.method.upper() == 'POST':
            return
        if request.path_info.startswith(settings.STATIC_URL):
            return
        if request.path_info.startswith(settings.MEDIA_URL):
            return

        for regex in settings.CANONICAL_URL_IGNORE_PATTERNS:
            if re.search(regex, request.path_info):
                return

        lang = translation.get_language_from_request(request)
        request_url = request.META['PATH_INFO']
        found_language = False
        for language in settings.CMS_FRONTEND_LANGUAGES:
            if request_url.startswith('/{0}/'.format(language)):
                found_language = True
                break

        if not found_language and settings.CMS_SEO_ROOT:
            return HttpResponseRedirect('/{0}{1}'.format(
                lang, request_url))


class VirtualAcademyMiddleware(object):
    """
    Redirects to first subchapter if any chapter or root page is requested.

    """
    def process_request(self, request):
        if 'admin' in request.path_info:
            return
        if not hasattr(request.current_page, 'get_root'):
            return
        if not request.current_page.get_root().reverse_id == 'subpages_root':
            return
        if request.current_page.is_leaf_node():
            return
        try:
            child = request.current_page.get_children()[0]
        except IndexError:
            return
        if child.is_leaf_node():
            return HttpResponseRedirect(child.get_absolute_url())
        try:
            child_child = child.get_children()[0]
        except IndexError:
            return
        return HttpResponseRedirect(child_child.get_absolute_url())
