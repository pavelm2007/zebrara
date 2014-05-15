# -*- coding: utf-8 -*-
import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, View, TemplateView, ListView, DetailView
from django import forms
from django.template import loader

from endless_pagination.views import AjaxListView
from braces.views import AjaxResponseMixin, JSONResponseMixin

from common.utils import paginate
from .forms import *
from .models import *


class WorksIndex(JSONResponseMixin, AjaxResponseMixin, ListView):
    model = Work
    template_name = 'works/list_objects.html'

    def render_to_response(self, context, **response_kwargs):
        ctx = dict()
        qs = self.model.filters.active_list().filter(is_work=True)[2:]
        work_per_page = 3
        work_paginator, work_page_obj, work_page = paginate(qs, work_per_page, self.request, param_name='work_page')
        work_objects = list(work_page_obj.object_list)
        ctx.update(
            {
                'work_paginator': work_paginator,
                'work_page_obj': work_page_obj,
                'work_list': work_objects,
            }
        )
        template = loader.render_to_string(self.template_name, ctx)
        return self.render_json_response({'template': template, })


class ExampleList(JSONResponseMixin, AjaxResponseMixin, ListView):
    model = Work
    template_name = 'works/example_list.html'
    content_type = None

    def get_content_type(self):
        if self.request.is_ajax():
            return u'application/json'
        else:
            return None

    def get_queryset(self, **kwargs):
        pk = self.kwargs.get('pk')
        qs = self.model.filters.active_list().filter(service__pk=pk).filter(is_example=True)
        return qs

    def render_to_response(self, context, **response_kwargs):
        res = {'object_list': self.get_queryset()}
        template = loader.render_to_string(self.template_name, res)
        return self.render_json_response({'template': template, })


class ExampleServiceList(JSONResponseMixin, AjaxResponseMixin, ListView):
    model = Work
    template_name = 'works/example_service_list.html'
    content_type = None

    def get_content_type(self):
        if self.request.is_ajax():
            return u'application/json'
        else:
            return None

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        service = Service.objects.get(pk=pk)
        qs = self.model.filters.active_list().filter(service__pk=pk).filter(is_example=True)
        return qs

    def render_to_response(self, context, **response_kwargs):
        res = {'object_list': self.get_queryset()}
        template = loader.render_to_string(self.template_name, dictionary=res)
        return self.render_json_response({'template': template, })


class WorkDetail(JSONResponseMixin, AjaxListView, DetailView):
    content_type = None
    model = Work

    def get_context_data(self, **kwargs):
        ctx = super(WorkDetail, self).get_context_data(**kwargs)
        return ctx

    def get_content_type(self):
        if self.request.is_ajax():
            return u'application/json'
        else:
            return None

    def render_to_response(self, context, **response_kwargs):
        object = self.get_object()
        res = {'object': object, }
        template = loader.render_to_string('works/work_detail.html', res)
        return self.render_json_response({'template': template, })


class ExampleDetail(JSONResponseMixin, AjaxListView, DetailView):
    content_type = None
    model = Work

    def get_context_data(self, **kwargs):
        ctx = super(ExampleDetail, self).get_context_data(**kwargs)
        return ctx

    def get_content_type(self):
        if self.request.is_ajax():
            return u'application/json'
        else:
            return None

    def render_to_response(self, context, **response_kwargs):
        object = self.get_object()
        res = {'object': object, }
        template = loader.render_to_string('works/work_detail.html', res)
        return self.render_json_response({'template': template, })