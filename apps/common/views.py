# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, ListView, FormView, CreateView

from flatcontent.models import FlatContent
from common.utils import paginate

from events.models import *
from works.models import *
from flatpages.models import *
from feedback.models import *
from feedback.forms import *

from .models import *

__all__ = [
    'MainPage',
    'robots',
    'Error403',
    'Error404',
    'Error500',
]


class MainPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super(MainPage, self).get_context_data(**kwargs)
        event_list_little = Event.object_filter.live().all()[:2]
        event_list = Event.object_filter.live().all()[2:]
        work_list_little = Work.filters.active_list().filter(is_work=True)[:2]
        work_list = Work.filters.active_list().filter(is_work=True)[2:]
        service_list = Service.filters.active_list()
        per_page = 3
        paginator, page_obj, page = paginate(event_list, per_page, self.request)
        objects = list(page_obj.object_list)

        work_per_page = 3
        work_paginator, work_page_obj, work_page = paginate(work_list, work_per_page, self.request, param_name='work_page')
        work_objects = list(work_page_obj.object_list)

        try:
            contact_address = FlatContent.objects.get(slug='contact_address')
        except FlatContent.DoesNotExist:
            contact_address = None
        try:
            contact_text = FlatContent.objects.get(slug='contact_text')
        except FlatContent.DoesNotExist:
            contact_text = None
        form = FeedbackForm()
        ctx.update(
            {'paginator': paginator,
             'page_obj': page_obj,
             'event_list': objects,
             'event_list_little': event_list_little,

             #'event_list': event_list,
             'work_list_little':work_list_little,
             'work_paginator': work_paginator,
             'work_page_obj': work_page_obj,
             'work_list': work_objects,

             'service_list': service_list,
             'contact_text': contact_text,
             'contact_address': contact_address,
             'form': form,
            }
        )
        return ctx


class About(TemplateView):
    template_name = 'common/about.html'

    def get_context_data(self, **kwargs):
        ctx = super(About, self).get_context_data(**kwargs)
        try:
            about_text = FlatContent.objects.get(slug='about')
        except FlatContent.DoesNotExist:
            about_text = None
        action_list = Action.active.by_main()
        if action_list.count():
            ctx['action'] = action_list.latest('id')
        action_list = Action.active.by_active()
        if action_list.count():
            ctx['action'] = action_list.latest('id')
        page_css = 'about_page'
        ctx.update(
            {
                'about': about_text,
                'page_css': page_css,
                'white_bg': False,
            }
        )
        return ctx


class Contacts(TemplateView):
    template_name = 'common/contacts.html'

    def get_context_data(self, **kwargs):
        ctx = super(Contacts, self).get_context_data(**kwargs)
        try:
            contacts_text = FlatContent.objects.get(slug='contacts')
        except FlatContent.DoesNotExist:
            contacts_text = None
        page_css = 'contacts_page'
        ctx.update(
            {
                'contacts': contacts_text,
                'page_css': page_css,
                'white_bg': False,
            }
        )
        return ctx


def robots(request):
    from django.http import HttpResponse

    return HttpResponse("User-agent: *\nDisallow: /admin/\nSitemap: http://%s/sitemap.xml" % request.get_host(),
                        mimetype="text/plain")


class Error403(TemplateView):
    template_name = '404.html'


class Error404(TemplateView):
    template_name = '404.html'


class Error500(TemplateView):
    template_name = '500.html'