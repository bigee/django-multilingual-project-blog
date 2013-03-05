"""Translations for the apps that we use."""
from django.utils.translation import gettext_noop
from django.utils.translation import ugettext_lazy as _

from cmsplugin_blog.admin import EntryAdmin
from cmsplugin_blog.models import Entry
from multilingual_events.admin import EventAdmin
from document_library.admin import AttachmentInline


Entry._meta.get_field('tags').help_text = _(
    'Please enter all tags in English with lowercase letters only, separate'
    ' them with commas. You can translate tags in the tagging admin'
    ' <a href="/admin/tagging/tag/">here</a>.')


gettext_noop('Auth')
gettext_noop('auth')

gettext_noop('Cms')
gettext_noop('cms')

gettext_noop('Cmsplugin_Blog')
gettext_noop('cmsplugin_blog')

gettext_noop('Cmsplugin_Blog_Categories')
gettext_noop('cmsplugin_blog_categories')

gettext_noop('Cmsplugin_Filer_Image')
gettext_noop('cmsplugin_filer_image')

gettext_noop('Document_Library')
gettext_noop('document_library')

gettext_noop('Hero_Slider')
gettext_noop('hero_slider')

gettext_noop('Filer')
gettext_noop('filer')

gettext_noop('Multilingual_Events')
gettext_noop('multilingual_events')

gettext_noop('Sites')
gettext_noop('sites')


EntryAdmin.inlines = EntryAdmin.inlines[:] + [AttachmentInline]
EventAdmin.inlines = EventAdmin.inlines[:] + [AttachmentInline]
