from django.contrib import admin

from cmsplugin_blog.admin import EntryAdmin
from document_library.admin import AttachmentInline
from hero_slider.admin import SliderItemAdmin
from hero_slider.models import SliderItem
from multilingual_events.admin import EventAdmin

from .forms import CustomSliderItemAdminForm


class CustomSliderItemAdmin(SliderItemAdmin):
    form = CustomSliderItemAdminForm


EntryAdmin.inlines = EntryAdmin.inlines[:] + [AttachmentInline]
EventAdmin.inlines = EventAdmin.inlines[:] + [AttachmentInline]


admin.site.unregister(SliderItem)
admin.site.register(SliderItem, CustomSliderItemAdmin)
