"""Translations for the apps that we use."""
from django.contrib.contenttypes import generic
from django.utils.translation import gettext_noop

from document_library.models import Attachment, DocumentCategory
from multilingual_events.models import Event


Event.add_to_class('attachments', generic.GenericRelation(Attachment))


DocumentCategory.add_to_class('generic_position', generic.GenericRelation(
    'generic_positions.ObjectPosition'))


gettext_noop('Auth')
gettext_noop('auth')

gettext_noop('Cms')
gettext_noop('cms')

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
