# flake8: noqa
# -*- coding: utf-8 -*-
"""
Basically the only reason why we need this and the following migrations is,
that we can order the migrations without having to create incredible lots of
dependencies spread all over all apps, that are involved.

Like, when you add a needed_by or depends_on argument to any migration, you
include the requirement to install and migrate it, even if you don't want or
need the app. To avoid that, we work around like this.

"""
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('multilingual_events', '0037_auto__add_eventcategorytranslation__add_unique_eventcategorytranslatio'),
        ('document_library', '0021_migrate_placeholders'),
    )

    def forwards(self, orm):
        pass

    def backwards(self, orm):
        pass

    models = {

    }

    complete_apps = ['multilingual_project_blog']
