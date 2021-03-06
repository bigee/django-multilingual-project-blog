"""Templatetags for the multilingual_project_blog project."""
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils.translation import (
    get_language_from_request,
    get_language_info,
    ugettext_lazy as _,
)


from classytags.arguments import Argument, MultiValueArgument
from cms.templatetags.cms_tags import Placeholder, PlaceholderOptions
from multilingual_news.models import Category, NewsEntry
from multilingual_tags.models import Tag


register = template.Library()


@register.assignment_tag
def debug(obj):
    import ipdb; ipdb.set_trace() # BREAKPOINT
    return obj


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
    try:
        info = get_language_info(code)
    except Exception:
        info = {}
    return info


@register.assignment_tag
def get_absolute_url(obj):
    """
    Returns the absolute URL for the best matching language.

    If the object has a version in the currently activated language, that URL
    will be returned, otherwise the first language that can be found will be
    returned.

    :param entry: An entry instance.

    """
    return obj.get_absolute_url()


@register.assignment_tag
def get_first_gallery(entry):
    """Returns the first gallery plugin of a blog Entry."""
    for plugin in entry.content.get_plugins():
        if plugin.get_plugin_name().title() == 'Folder':
            return plugin
    return False


@register.assignment_tag
def get_person_info(person):
    result_parts = []
    if person.title:
        result_parts.append(u'{0}'.format(_(person.title)))
    if person.chosen_name:
        result_parts.append(u'{0}: {1}'.format(
            _('Nickname'), person.chosen_name))
    if person.role:
        result_parts.append(person.role.name)
    return ', '.join(result_parts)


@register.assignment_tag
def get_translation(obj, language_code):
    """Returns the object instance in a certain language."""
    try:
        obj_trans = obj.translations.get(language_code=language_code)
    except ObjectDoesNotExist:
        return obj
    return obj_trans


@register.assignment_tag()
def get_next_subchapter(current_page):
    """Returns the previous subchapter page, if available, otherwise None."""
    sibling = current_page.get_next_sibling()
    if sibling:
        return sibling
    parent_sibling = current_page.parent.get_next_sibling()
    if parent_sibling and parent_sibling.get_children():
        return parent_sibling.get_children()[0]
    return None


@register.assignment_tag()
def get_next_chapter(current_page):
    """returns the previous chapter page, if available, otherwise none."""
    next_sibling = current_page.parent.get_next_sibling()
    if not next_sibling:
        return None
    children = next_sibling.get_children()
    if children:
        return children[0]
    return None


@register.assignment_tag()
def get_previous_chapter(current_page):
    """returns the previous chapter page, if available, otherwise none."""
    previous_sibling = current_page.parent.get_previous_sibling()
    if not previous_sibling:
        return None
    children = previous_sibling.get_children()
    if children:
        return children[0]
    return None


@register.assignment_tag()
def get_previous_subchapter(current_page):
    """Returns the previous subchapter page, if available, otherwise None."""
    sibling = current_page.get_previous_sibling()
    if sibling:
        return sibling
    parent_sibling = current_page.parent.get_previous_sibling()
    if parent_sibling and parent_sibling.get_children():
        return parent_sibling.get_children().last()
    return None


@register.assignment_tag()
def is_level1_selected(node):
    """Returns the level1 page for the given menu node."""
    if not node.children and node.selected:
        return True
    for child in node.children:
        if child.selected:
            return True
    return False


@register.assignment_tag()
def is_root_page_selected(current_page, menu_id):
    """Returns ``True`` if the current page has the given menu id."""
    return current_page.reverse_id == menu_id


@register.assignment_tag
def placeholder_has_plugins(placeholder):
    """
    Returns ``True`` if the given placeholder produces output.

    :param placeholders: A queryset of placeholders.
    :param placeholder_name: The placeholder to be searched for in the qs.

    """
    return placeholder.cmsplugin_set.count() > 0


@register.inclusion_tag(
    'multilingual_news/category_links_snippet.html',
    takes_context=True)
def render_categories(context, exclude_empty=False):
    """Renders the category liks."""
    qs = Category.objects.annotate(num_posts=Count('newsentries'))
    request = context.get('request')
    language = getattr(request, 'LANGUAGE_CODE', None)
    if language:
        qs = qs.filter(translations__language_code=language)
    if exclude_empty:
        qs = qs.exclude(num_posts=0)
    context.update({'categories': qs, })
    return context


@register.inclusion_tag('multilingual_news/entry_languages_snippet.html',
                        takes_context=True)
def render_entry_languages(context, entry):
    """
    Renders the available languages for a given EntryTitle.

    :param entry_title: An EntryTitle instance.

    """
    excluded_language = context.get('SESSION_LANGUAGE', entry.language_code)
    context.update({
        'entry_languages': entry.translations.exclude(
            language_code=excluded_language),
    })
    return context


@register.inclusion_tag('multilingual_news/entry_tag_links_snippet.html',
                        takes_context=True)
def render_entry_tag_links(context, entry):
    """
    Renders the tag links for a given entry.

    :param entry: An Entry instance.

    """
    context.update({
        'tags': Tag.objects.get_for_obj(entry)
    })
    return context


@register.inclusion_tag('multilingual_news/latest_entries_links_snippet.html',
                        takes_context=True)
def render_latest_entries_links(context, request=None):
    """
    Renders the links to the 5 latest entries.

    """
    qs = NewsEntry.objects.published()
    context.update({
        'entries': qs[:5]
    })
    return context


@register.inclusion_tag('multilingual_news/tag_links_snippet.html',
                        takes_context=True)
def render_tags(context):
    request = context["request"]
    language = get_language_from_request(request)
    object_list = NewsEntry.objects.published(language)
    context.update({
        'tag_list': [{
            'tag': tag, 'tagged_items': object_list.filter(
                tags__tag__slug=tag.slug).count()}
            for tag in Tag.objects.get_for_queryset(object_list)]
    })
    return context
