"""Templatetags for the multilingual_project_blog project."""
from django import template
from django.db.models import Count
from django.utils import translation, timezone
from django.utils.translation import get_language_info

from classytags.arguments import Argument, MultiValueArgument
from cms.templatetags.cms_tags import Placeholder, PlaceholderOptions
from cms.utils import get_language_from_request
from cmsplugin_blog.models import Entry, EntryTitle
from cmsplugin_blog_categories.models import Category
from cmsplugin_blog_language_publish.models import EntryLanguagePublish
from simple_translation.middleware import filter_queryset_language
from tagging.models import Tag


register = template.Library()


class PlaceholderAs(Placeholder):
    name = 'placeholder_as'
    options = PlaceholderOptions(
        Argument('name', resolve=False),
        MultiValueArgument('extra_bits', required=False, resolve=False),
        'as',
        Argument('varname', resolve=False),
        blocks=[
            ('endplaceholder', 'nodelist'),
        ]
    )

    def render_tag(self, context, name, extra_bits, varname, nodelist=None):
        output = super(PlaceholderAs, self).render_tag(
            context=context, name=name, extra_bits=extra_bits)
        if varname:
            context[varname] = output
            return ''
        return ''
register.tag(PlaceholderAs)


@register.assignment_tag
def add_to_context(obj):
    """
    Adds the given object to the template context.

    """
    return obj


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


@register.simple_tag
def get_entry_count_for_category(category, language):
    """Returns the amount of published entries in a category for a language."""
    qs = EntryLanguagePublish.objects.filter(
        is_published=True,
        entry_title__entry__categories__category=category,
        entry_title__language=language).count()
    return qs


@register.assignment_tag
def get_first_gallery(entry):
    """Returns the first gallery plugin of a blog Entry."""
    placeholder = entry.placeholders.get(slot='content')
    for plugin in placeholder.get_plugins():
        if plugin.get_plugin_name().title() == 'Folder':
            return plugin
    return False


@register.assignment_tag
def placeholder_has_plugins(placeholders, placeholder_name):
    """
    Returns ``True`` if the given placeholder produces output.

    :param placeholders: A queryset of placeholders.
    :param placeholder_name: The placeholder to be searched for in the qs.

    """
    ph = placeholders.get(slot=placeholder_name)
    return ph.cmsplugin_set.all().count() > 0


@register.inclusion_tag(
    'cmsplugin_blog_categories/category_links_snippet.html',
    takes_context=True)
def render_categories(context, exclude_empty=False):
    """Renders the category liks."""
    qs = Category.objects.annotate(num_posts=Count('entry_categories'))
    if exclude_empty:
        qs = qs.exclude(num_posts=0)
    request = context.get('request')
    language = getattr(request, 'LANGUAGE_CODE', None)
    if language:
        qs = qs.filter(
            entry_categories__entry__entrytitle__language=language,
            entry_categories__entry__entrytitle__is_published__is_published=
            True)
    context.update({'categories': qs, })
    return context


@register.inclusion_tag('cmsplugin_blog/entry_languages_snippet.html',
                        takes_context=True)
def render_entry_languages(context, entry_title):
    """
    Renders the available languages for a given EntryTitle.

    :param entry_title: An EntryTitle instance.

    """
    qs = EntryTitle.objects.filter(
        entry=entry_title.entry, is_published__is_published=True)
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


@register.inclusion_tag('cmsplugin_blog/tag_links_snippet.html',
                        takes_context=True)
def render_tags(context):
    request = context["request"]
    language = get_language_from_request(request)
    filters = dict(entrytitle__is_published=True, pub_date__lte=timezone.now(),
                   entrytitle__language=language)
    context.update({
        'tags': Tag.objects.usage_for_model(Entry, filters=filters)
    })
    return context
