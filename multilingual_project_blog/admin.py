from cmsplugin_blog.admin import EntryAdmin
from multilingual_events.admin import EventAdmin
from document_library.admin import AttachmentInline


EntryAdmin.inlines = EntryAdmin.inlines[:] + [AttachmentInline]
EventAdmin.inlines = EventAdmin.inlines[:] + [AttachmentInline]
