"""Templatetags for the multilingual_project_blog project."""
from django import template
from django.utils import translation
from django.utils.translation import get_language_info

from cmsplugin_blog.models import Entry, EntryTitle
from simple_translation.middleware import filter_queryset_language
from tagging.models import Tag


register = template.Library()


@register.assignment_tag
def custom_get_language_info(language_code):
    """
    Returns the language info for the given language code.

    This is a wrapper around the original method which takes care to convert
    language codes that have more than two characters into their correct
    versions.

    """
    code = language_code
    if code == 'zh':
        code = 'zh-cn'
    return get_language_info(code)


@register.assignment_tag
def get_absolute_url(obj):
    """
    Returns the absolute URL for the best matching language.

    If the object has a version in the currently activated language, that URL
    will be returned, otherwise the first language that can be found will be
    returned.

    :param entry: An entry instance.

    """
    current_lang = translation.get_language()
    if isinstance(obj, Entry):
        try:
            title = obj.entrytitle_set.get(language=current_lang)
        except EntryTitle.DoesNotExist:
            title = obj.entrytitle_set.all()[0]
        return title.get_absolute_url()
    return obj.get_absolute_url()


@register.assignment_tag
def get_first_gallery(entry):
    """Returns the first gallery plugin of a blog Entry."""
    placeholder = entry.placeholders.get(slot='content')
    for plugin in placeholder.get_plugins():
        if plugin.get_plugin_name().title() == 'Folder':
            return plugin
    return False


@register.inclusion_tag('cmsplugin_blog/entry_languages_snippet.html',
                        takes_context=True)
def render_entry_languages(context, entry_title):
    """
    Renders the available languages for a given EntryTitle.

    :param entry_title: An EntryTitle instance.

    """
    qs = EntryTitle.objects.filter(entry=entry_title.entry)
    qs = qs.exclude(language=entry_title.language)
    context.update({
        'entry_languages': qs,
    })
    return context


@register.inclusion_tag('cmsplugin_blog/entry_tag_links_snippet.html',
                        takes_context=True)
def render_entry_tag_links(context, entry):
    """
    Renders the tag links for a given entry.

    :param entry: An Entry instance.

    """
    context.update({
        'tags': Tag.objects.get_for_object(entry)
    })
    return context


@register.inclusion_tag('cmsplugin_blog/latest_entries_links_snippet.html',
                        takes_context=True)
def render_latest_entries_links(context, request=None):
    """
    Renders the links to the 5 latest entries.

    """
    qs = Entry.published.all()
    qs = filter_queryset_language(request, qs)
    context.update({
        'entries': qs[:5]
    })
    return context
