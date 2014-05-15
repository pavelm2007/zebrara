# -*- coding: utf-8 -*-
from django.forms import ModelForm, CharField, ImageField, Textarea

from cked.widgets import CKEditorWidget
from sorl.thumbnail.admin.current import AdminImageWidget

from .models import Event


class EventForm(ModelForm):
    text = CharField(label=u'Текст', widget=CKEditorWidget())
    #image = ImageField(label=u'Изображение', widget=AdminImageWidget(), required=False)

    class Meta:
        model = Event

