from django.contrib import admin

from cmsplugin_blog.admin import EntryAdmin
from document_library.admin import AttachmentInline, DocumentCategoryAdmin
from document_library.models import DocumentCategory
from generic_positions.admin import GenericPositionsAdmin
from hero_slider.admin import SliderItemAdmin
from hero_slider.models import SliderItem
from multilingual_events.admin import EventAdmin

from .forms import CustomSliderItemAdminForm


class CustomSliderItemAdmin(SliderItemAdmin):
    form = CustomSliderItemAdminForm


class OrderedDocumentCategoryAdmin(DocumentCategoryAdmin,
                                   GenericPositionsAdmin):
    """Extended ``DocumentCategoryAdmin``."""
    pass


EntryAdmin.inlines = EntryAdmin.inlines[:] + [AttachmentInline]
EventAdmin.inlines = EventAdmin.inlines[:] + [AttachmentInline]


admin.site.unregister(SliderItem)
admin.site.register(SliderItem, CustomSliderItemAdmin)

admin.site.unregister(DocumentCategory)
admin.site.register(DocumentCategory, OrderedDocumentCategoryAdmin)
