# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from django.template import loader

from braces.views import AjaxResponseMixin, JSONResponseMixin

from common.utils import paginate
from .models import *

__all__ = [
    'EventList',
    'EventDetail',
]


class EventMixin(object):
    def get_context_data(self, **kwargs):
        ctx = super(EventMixin, self).get_context_data(**kwargs)
        return ctx


class EventList(JSONResponseMixin, AjaxResponseMixin, ListView):
    model = Event
    template_name = 'events/list_objects.html'
    content_type = None

    def get_content_type(self):
        if self.request.is_ajax():
            return u'application/json'
        else:
            return None

    def get_context(self):
        ctx = dict()
        qs = self.model.object_filter.live()[2:]
        per_page = 3
        paginator, page_obj, page = paginate(qs, per_page, self.request)
        objects = list(page_obj.object_list)
        ctx.update(
            {
                'paginator': paginator,
                'page_obj': page_obj,
                'objects': objects,
            }
        )
        return ctx
        #return qs

    def render_to_response(self, context, **response_kwargs):
        templ = loader.render_to_string('events/list_objects.html', dictionary=self.get_context())
        return self.render_json_response({'template': templ, })

    def get_context_data(self, **kwargs):
        ctx = super(EventList, self).get_context_data(**kwargs)
        return ctx


class EventDetail(JSONResponseMixin, AjaxResponseMixin, DetailView):
    model = Event
    template_name = 'events/detail_object.html'
    content_type = None

    def get_context_data(self, **kwargs):
        ctx = super(EventDetail, self).get_context_data(**kwargs)
        return ctx

    def get_content_type(self):
        if self.request.is_ajax():
            return u'application/json'
        else:
            return None

    def render_to_response(self, context, **response_kwargs):
        object = self.get_object()
        res = {'object':object,}
        template = loader.render_to_string('events/detail.html', res)

        return self.render_json_response({'template':template,})