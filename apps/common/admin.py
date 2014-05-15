# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.contrib.contenttypes import generic
#from django_markdown.widgets import MarkdownWidget

from flatcontent.models import FlatContent
from cked.widgets import CKEditorWidget

from sorl.thumbnail.admin import AdminImageMixin

from .forms import ImageForm, FlatContentForm
from .models import *
from .widget import AdminImageWidget


class FlatContentAdminCustom(admin.ModelAdmin):
    form = FlatContentForm


admin.site.unregister(FlatContent)
admin.site.register(FlatContent, FlatContentAdminCustom)


class PhotoAdmin(admin.ModelAdmin):
    form = ImageForm
    model = Photo
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}


admin.site.register(Photo, PhotoAdmin)


class PhotoStakedAdmin(generic.GenericTabularInline):
    form = ImageForm
    model = Photo
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}


