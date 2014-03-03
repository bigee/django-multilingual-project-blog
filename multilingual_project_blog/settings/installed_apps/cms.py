"""Settings for the ``django-cms`` app."""
gettext = lambda s: s


CMS_SOFTROOT = True
CMS_PERMISSION = False
CMS_SEO_FIELDS = True
CMS_MENU_TITLE_OVERWRITE = True
CMS_SEO_ROOT = True
CMS_SEO_FIELDS = True

CMS_FRONTEND_LANGUAGES = ('en', 'zh', )

CMS_TEMPLATES = (
    ('cms/home.html', 'Homepage'),
    ('cms/standard.html', 'Page With Submenu'),
    ('cms/standard_without_submenu.html', 'Page Without Submenu'),
    ('multilingual_news/newsentry_list.html', 'Blog'),
    ('multilingual_events/event_list.html', 'Events'),
    ('good_practice_examples/examples_list.html', 'Good practice examples'),
)

CMS_PLACEHOLDER_CONF = {
    'conference': {
        'plugins': (
            'EventAgendaDayPlugin', 'EventAgendaSessionPlugin',
            'EventAgendaTalkPlugin'),
        'name': gettext('Conference'),
    },
}
