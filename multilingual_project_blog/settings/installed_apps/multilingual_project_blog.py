"""Settings for the ``multilingual_project_blog`` app."""
CANONICAL_URL_IGNORE_PATTERNS = [
    r'\.ico',
    r'\.ics',
    r'/ctype/$',
]


HERO_SLIDER_APPS_MODELS_LIST = [
    ('cmsplugin_blog', 'entry'),
    ('document_library', 'document'),
    ('multilingual_events', 'event'),
]
