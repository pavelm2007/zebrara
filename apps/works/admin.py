# -*- coding: utf-8 -*-
from django.contrib import admin

from feincms.admin import tree_editor
from sorl.thumbnail.admin import AdminImageMixin

from .forms import *
from .models import *


class ServiceAdmin(AdminImageMixin, tree_editor.TreeEditor):
    form = ServiceForm
    # specify pixel amount for this ModelAdmin only:
    list_display = ('name', 'is_active', 'thumbnail')
    list_display_links = ('name', 'thumbnail',)
    mptt_level_indent = 20
    fieldsets = (
        (None, {
            'fields': (('is_active', 'position'), 'image', 'name', 'short_text', 'text', 'price')
        }),
    )


admin.site.register(Service, ServiceAdmin)


class WorkMediaInline(AdminImageMixin, admin.TabularInline):
    model = WorkMedia
    sortable_field_name = "position"
    extra = 0


class WorkAdmin(AdminImageMixin, admin.ModelAdmin):
    form = WorkForm
    list_display = ('thumbnail', 'name', 'is_active', 'is_work', 'is_example',)
    list_editable = ('is_active', 'is_work', 'is_example',)
    list_display_links = ('name', )
    list_per_page = 50
    search_fields = ('name', 'text', )
    list_filter = ('is_active',)
    fieldsets = (
        (None, {
            'fields': (('is_active', 'position', 'is_work', 'is_example'), 'service', 'name', 'short_text', 'text', 'date',)
        }),
    )
    inlines = [WorkMediaInline, ]


admin.site.register(Work, WorkAdmin)


class ExampleMediaInline(AdminImageMixin, admin.TabularInline):
    model = ExampleMedia
    sortable_field_name = "position"
    extra = 0


class ExampleAdmin(AdminImageMixin, admin.ModelAdmin):
    form = ExampleForm
    list_display = ('name',  'is_active',)
    list_display_links = ('name',  'is_active',)
    list_per_page = 50
    search_fields = ('name', 'text', )
    list_filter = ('is_active',)
    fieldsets = (
        (None, {
            'fields': (('is_active', 'position'), 'service', 'name', 'text', 'date',)
        }),
    )
    inlines = [ExampleMediaInline ]

#admin.site.register(Example, ExampleAdmin)