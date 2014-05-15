# -*- coding: utf-8 -*-
from django import forms

from cked.widgets import CKEditorWidget

from .models import Service, Work, Example

__all__ = [
    'ServiceForm',
    'ExampleForm',
    'WorkForm',
]


class ServiceForm(forms.ModelForm):
    text = forms.CharField(label=u'Текст', widget=CKEditorWidget, required=False)

    class Meta:
        model = Service

class ExampleForm(forms.ModelForm):
    text = forms.CharField(label=u'Текст', widget=CKEditorWidget, required=False)

    class Meta:
        model = Example

class WorkForm(forms.ModelForm):
    text = forms.CharField(label=u'Текст', widget=CKEditorWidget, required=False)

    class Meta:
        model = Work

