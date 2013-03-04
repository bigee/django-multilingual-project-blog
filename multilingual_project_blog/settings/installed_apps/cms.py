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
    ('cms/standard.html', 'Standard'),
    ('cmsplugin_blog/cmsplugin_blog_base.html', 'Blog'),
    ('multilingual_events/event_list.html', 'Events'),
)
