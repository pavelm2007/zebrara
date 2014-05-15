# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets
from .models import Feedback

__all__ = [
    'FeedbackForm',
]


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        #self.fields['comment'] = forms.CharField(widget=widgets.Textarea(attrs={'cols': '54', 'rows': '5'}))
        self.fields['comment'].widget.attrs.update({'cols': '60', 'rows': '5'})
        self.fields['title'].widget.attrs.update({'style': 'width: 450px;'})
        #for field in self.fields:
        #    self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Feedback
        fields = ('name', 'phone', 'email', 'title', 'comment',)


