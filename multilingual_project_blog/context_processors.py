"""Context processors for the ``bigEE`` project."""
from django.utils import translation

from . import app_settings


def project_settings(request):
    """
    Adds some settings values to all templates.

    ENVIRONMENT
    -----------

    Useful if you want to hide certain things on production for the time being.

    SITE_URL
    --------

    I hate to use the sites framework for this. Enter the full domain here,
    i.e. ``http://example.com``

    SITE_URL_NAME
    -------------

    The URL as it should be shown between the <a> tag, i.e. ``www.example.com``

    INFO_EMAIL
    ----------

    The info email you would like to display.

    """
    return {
        'ENVIRONMENT': app_settings.ENVIRONMENT,
        'SITE_URL': app_settings.SITE_URL,
        'SITE_URL_NAME': app_settings.SITE_URL_NAME,
        'INFO_EMAIL': app_settings.INFO_EMAIL,
    }


def session_language(request):
    """
    Adds the variable {{ SESSION_LANGUAGE }} to all templates.

    We need this because sometimes we want to display pages with two languages:

    1. The interface should always be the language that the user has chosen
       as his preference.
    2. The content of a blog post can be viewed in a different translation if
       available.

    """
    if 'django_language' in request.session:
        lang = request.session['django_language']
    else:
        lang = translation.get_language_from_request(request)
        request.session['django_language'] = lang
    return {'SESSION_LANGUAGE': lang, }
