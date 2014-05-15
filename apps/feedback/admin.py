# -*- coding: utf-8 -*-
from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .forms import *
from .models import *


class FeedbackAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('created', 'name', 'phone', 'email',)
    list_display_links = ('created', 'name', 'phone', 'email',)
    list_per_page = 50
    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'email', 'title', 'comment',)
        }),
    )


admin.site.register(Feedback, FeedbackAdmin)