"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

"""

from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for buildee.
    """
    def init_with_context(self, context):
        self.children += [
            modules.ModelList(_('Blog'), [
                'cmsplugin_blog.models.Entry',
                'cmsplugin_blog_categories.models.Category',
                'tagging.models.Tag']),
            modules.ModelList(_('Filer'), [
                'cmsplugin_filer_image*',
                'filer*']),
            modules.ModelList(_('Document Library'), [
                'document_library*']),
            modules.ModelList(_('Hero Slider'), [
                'hero_slider*']),
            modules.ModelList(_('Events'), [
                'multilingual_events*']),
            modules.ModelList(_('CMS'), [
                'cms.plugins.snippet*',
                'cms.models.page*']),
            modules.ModelList(_('People'), [
                'people.models.Person']),
            modules.ModelList(_('Organizations'), [
                'multilingual_orgs.models.Organizatio*']),
            modules.ModelList(_('Organizations'), [
                'multilingual_orgs.models.Organizatio*']),
            modules.ModelList(_('Roadmap'), [
                'roadmap.models*']),
        ]


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for buildee.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
