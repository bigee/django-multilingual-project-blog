"""Middlewares for the ``multilingual_project_blog`` app."""
import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation

from cms.middleware import multilingual
from cms.utils.i18n import get_default_language
from cms.test_utils.util.context_managers import SettingsOverride


def get_language_from_request(cls, request):
    """
    Customized version of this method on MultilingualURLMiddleware.

    Ignores the language prefix on the URL.

    """
    prefix = multilingual.has_lang_prefix(request.path_info)
    lang = None
    if prefix:
        request.path = "/" + "/".join(request.path.split("/")[2:])
        request.path_info = "/" + "/".join(request.path_info.split("/")[2:])
        return prefix
    if not lang:
        languages = []
        for frontend_lang in settings.CMS_FRONTEND_LANGUAGES:
            languages.append((frontend_lang, frontend_lang))
        with SettingsOverride(LANGUAGES=languages):
            lang = translation.get_language_from_request(request)
    if not lang:
        lang = get_default_language()
    old_lang = None
    if hasattr(request, 'session') and request.session.get(
            'django_language', None):
        old_lang = request.session['django_language']
    if not old_lang and hasattr(request, 'COOKIES') and request.COOKIES.get(
            settings.LANGUAGE_COOKIE_NAME, None):
        old_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    if old_lang != lang:
        if hasattr(request, 'session'):
            request.session['django_language'] = lang
    return lang


# Creating a sub class does not work. So let's just patch the original.
multilingual.MultilingualURLMiddleware.get_language_from_request = \
    get_language_from_request


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


class SwitchLanguageMiddleware(object):
    """
    Saves new language into the session when a user uses the language choser.

    """
    def process_request(self, request):
        lang = request.GET.get('switch-language')
        if lang:
            request.session['django_language'] = lang
            translation.activate(lang)
            request_url = request.META['PATH_INFO']
            # Let's reirect to get rid of the GET parameter
            return HttpResponseRedirect(request_url)
