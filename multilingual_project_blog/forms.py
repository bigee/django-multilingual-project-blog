from django import forms
from django.conf import settings
from django.db.models import Q

from simple_translation.forms import TranslationModelForm

from hero_slider.models import SliderItem


class CustomSliderItemAdminForm(TranslationModelForm):
    class Meta:
        model = SliderItem

    def __init__(self, *args, **kwargs):
        super(CustomSliderItemAdminForm, self).__init__(*args, **kwargs)
        qs = self.fields['content_type'].queryset
        q_objects = Q()
        for app_label, model in settings.HERO_SLIDER_APPS_MODELS_LIST:
            q_objects.add(Q(app_label=app_label, model=model), Q.OR)
        qs = qs.filter(q_objects)
        self.fields['content_type'].queryset = qs
