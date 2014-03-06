"""Custom news feeds for the multilingual project blog."""
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from multilingual_news.feeds import NewsEntriesFeed


class CustomNewsEntriesFeed(NewsEntriesFeed):
    """
    Customized to get the universal content link, that is independent of the
    currently active language.

    Chooses the correct fallback language in case the active one does not
    exist.

    """
    def item_link(self, item):
        language = None
        try:
            language = item.language_code
            slug = item.slug
        except ObjectDoesNotExist:
            pass
        else:
            return reverse('news_detail', kwargs={'slug': slug})
        if language is None:
            try:
                trans = item.translations.get(language_code='en')
            except ObjectDoesNotExist:
                pass
            else:
                language = trans.language_code
                slug = trans.slug
        if language is None:
            language = item.translations.all()[0].language_code
            slug = item.translations.all()[0].slug
        return '{0}?lang={1}'.format(reverse('news_detail', kwargs={
            'slug': slug}), language)
