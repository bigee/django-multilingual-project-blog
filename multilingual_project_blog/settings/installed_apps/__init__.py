"""
INSTALLED_APPS of the project.

Split up into sup-lists so that we can exlude them from the coverage report.

"""
PROJECT_BLOG_APPS = [
    # admin tools
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    # Must come before all other apps
    'multilingual_project_blog',

    # django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',

    # Other important apps
    'django_extensions',
    'django_libs',
    'south',
    'rosetta',
    'document_library',
    'hero_slider',
    'multilingual_events',
    'people',
    'localized_names',
    'roadmap',

    # django-cms related apps
    'cms',
    'sekizai',
    'mptt',
    'menus',
    'cms.plugins.text',
    'cms.plugins.link',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'cmsplugin_link_extended',

    # blog related apps
    'cmsplugin_blog',
    'djangocms_utils',
    'simple_translation',
    'tagging',
    'missing',
    'cmsplugin_blog_categories',
    'cmsplugin_blog_images',
    'cmsplugin_blog_authors',
    'cmsplugin_blog_language_publish',
    'tagging_translated',
    'multilingual_orgs',

    # django-filer related apps
    'filer',
    'cmsplugin_filer_file',
    'cmsplugin_filer_image',
    'cmsplugin_filer_folder',
    'easy_thumbnails',
    'cmsplugin_filer_image_translated',
]


def add_project_blog_apps(installed_apps):
    result = list(installed_apps)
    for app in PROJECT_BLOG_APPS:
        if app not in result:
            result.append(app)
    return result


from .multilingual_project_blog import *  # NOQA
from .debug_toolbar import *  # NOQA
from .cms import *  # NOQA
from .cmsplugin_blog import *  # NOQA
from .registration import *  # NOQA
from .rosetta import *  # NOQA
from .admin_tools import *  # NOQA
from .localized_names import *  # NOQA
