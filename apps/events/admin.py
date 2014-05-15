# -*- coding: utf-8 -*-
from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .forms import EventForm
from .models import *


class EventMediaInline(AdminImageMixin, admin.TabularInline):
    model = EventMedia
    sortable_field_name = "position"
    extra = 0


class EventAdmin(AdminImageMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = EventForm
    list_display = ('title', 'is_active', 'position', 'published', 'status',)
    list_editable = ('position',)
    list_display_links = ('title', 'published',)
    list_per_page = 50
    search_fields = ('title', 'short_text', 'text',)
    list_filter = ('is_active',)
    fieldsets = (
        (None, {
            'fields': (('is_active', 'position', 'published', 'status'), 'title', 'slug', 'short_text', 'text',)
        }),
    )
    #inlines = [EventMediaInline, ]


admin.site.register(Event, EventAdmin)