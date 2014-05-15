# -*- coding: utf-8 -*-
import json
from django.views.generic import CreateView, TemplateView, FormView
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.utils import simplejson as json

from common.utils import JsonResponse
from .forms import *
from .models import *


def feedback_save(request):
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        fields = form.cleaned_data
        feedback = form.save(commit=False)
        feedback.save()
        if request.is_ajax():
            return JsonResponse({'status': True})

    if request.is_ajax():
        return JsonResponse({'status': False, 'errors': form.errors})

class Feedback(CreateView):
#class Feedback(JSONResponseMixin, AjaxResponseMixin, CreateView):
    model = Feedback
    success_url = '/'

    #def get_success_url(self):
    #    return reverse('feedback:sent')
    #
    #def render_to_response(self, **kwargs):
    #    if self.request.is_ajax():
    #        # Don't really know if objects will take a list, a queryset, any iterable or even a single object
    #        template = loader.render_to_string('feedback/sended.html')
    #
    #        return self.render_json_response({'template': template, })
    #    else:
    #        return CreateView.render_to_response(self, **kwargs)

    def form_valid(self, form):
        """
        If the request is ajax, save the form and return a json response.
        Otherwise return super as expected.
        """
        #if self.request.is_ajax():
        self.object = form.save()
        return HttpResponse(json.dumps("success"), mimetype="application/json")
        #return super(Feedback, self).form_valid(form)
        #return HttpResponseRedirect(reverse('feedback:sent'))

    def form_invalid(self, form):
        """
        We haz errors in the form. If ajax, return them as json.
        Otherwise, proceed as normal.
        """
        #if self.request.is_ajax():
        #    return HttpResponseBadRequest(json.dumps(form.errors),
        #        mimetype="application/json")
        #return super(Feedback, self).form_invalid(form)
        return HttpResponseRedirect(reverse('feedback:sent'))

    #def get_content_type(self):
    #    if self.request.is_ajax():
    #        return u'application/json'
    #    else:
    #        return None
    #
    #def form_invalid(self, form):
    #    #super(Feedback,self).form_invalid(form)
    #    return reverse('feedback:error_send')

class Sended(TemplateView):
    template_name = 'feedback/sended.html'

class ErrorSend(TemplateView):
    template_name = 'feedback/error_send.html'

#class Sended(JSONResponseMixin, AjaxResponseMixin, TemplateView):
#    template_name = 'feedback/sended.html'
#
#    def render_to_response(self, context, **response_kwargs):
#        template = loader.render_to_string('feedback/sended.html')
#        return self.render_json_response({'template': template, })

#class ErrorSend(JSONResponseMixin, AjaxResponseMixin, TemplateView):
#    template_name = 'feedback/error_send.html'
#
#    def render_to_response(self, context, **response_kwargs):
#        template = loader.render_to_string('feedback/error_send.html')
#        return self.render_json_response({'template': template, })


