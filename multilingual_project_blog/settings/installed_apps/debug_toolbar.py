"""Settings for the ``debug_toolbar`` app."""
DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': 'lcfc.settings.local_settings.show_toolbar',
}
