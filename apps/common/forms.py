# -*- coding: utf-8 -*-
from django import forms
from flatcontent.models import FlatContent
from cked.widgets import CKEditorWidget

from .widget import AdminImageWidget
from .models import *


class FlatContentForm(forms.ModelForm):
    content = forms.CharField(label=u'Текст', widget=CKEditorWidget)

    class Meta:
        model = FlatContent

    def __init__(self, *args, **kwargs):
        super(FlatContentForm, self).__init__(*args, **kwargs)
        self.fields['slug'].help_text = u'Имя, под которым значение извлекается в шаблоне.'


class ImageForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'main_image', 'title', )
        widgets = {
            'image': AdminImageWidget,
        }

