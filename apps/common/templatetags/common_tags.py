# -*- coding: utf-8 -*-
import re
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeData
from django import template
from django.core.urlresolvers import reverse
from django.utils.text import normalize_newlines


register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    {% get_verbose_field_name test_instance "name" %}
    """
    return instance._meta.get_field(field_name).verbose_name.title()


@register.filter(name='access')
def access(value, arg):
    return value[arg]


@register.tag
def toggle(parser, token):
    """
        <li {% active request index %} ><a href="{% url index %}">Главная</a></li>
        <li {% active request news_index %}><a href="{% url news_index %}">Новости</a></li>
    """

    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    return ToggleNavSelectedNode(args[1:])


class ToggleNavSelectedNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        if context['request'].path == reverse(self.name[1]) or re.search('order', context['request'].path):
            return u''
        else:
            return 'toggle'

@register.tag
def active(parser, token):
    """
        <li {% active request index %} ><a href="{% url index %}">Главная</a></li>
        <li {% active request news_index %}><a href="{% url news_index %}">Новости</a></li>
    """

    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    return NavSelectedNode(args[1:])


class NavSelectedNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        if context['request'].path == reverse(self.name[1]):
            return u'class = "active"'
        else:
            return ''


@register.simple_tag
def active_contain(request, pattern):
    import re

    if re.search(pattern, request.path):
        return "class = 'active'"
    return ''


@register.filter
def strip_zeros(val):
    val = str(val)
    symbols = ('0', '.', ',')
    if '.' in val:
        while val[-1] in symbols:
            if val[-1] == '.':
                val = val[:-1]
                break
            val = val[:-1]
    return val


@register.filter
@stringfilter
def startswith(value, arg):
    try:
        arg = str(arg)
    except (ValueError, TypeError):
        return value
    return value.startswith(arg)


startswith.is_safe = True



@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def spacify(value, autoescape=None):
    autoescape = autoescape and not isinstance(value, SafeData)
    value = normalize_newlines(value)
    if autoescape:
        value = escape(value)
    value = mark_safe(value.replace('  ', ' &nbsp;'))
    #return mark_safe(value.replace('\n', '<br />'))
    return mark_safe(value)

@register.filter
def intspace(value, arg=' '):
    '''
    Converts an integer to a string containing spaces every three digits.
    For example, 3000 becomes '3 000' and 45000 becomes '45 000'.
    '''
    orig = force_unicode(value)
    new = re.sub('^(-?\d+)(\d{3})', '\g<1>%s\g<2>' % arg, orig)
    if orig == new:
        return mark_safe(new)
    else:
        return intspace(new, arg)


intspace.is_safe = True


@register.simple_tag(takes_context=True)
def url_add_query(context, **kwargs):
    '''
        <h3>Page: {{ page.number }} of {{ page.paginator.num_pages }}</h3>
        {% if page.has_previous or page.has_next %}
        <div>
            {% if page.has_previous %}
                <a href="{% url_add_query page=page.previous_page_number %}">
            {% endif %}&laquo; Previous {% if page.has_previous %}</a>{% endif %} |
            {% if page.has_next %}
                <a href="{% url_add_query page=page.next_page_number %}">
            {% endif %} Next &raquo;
            {% if page.has_next %}</a>{% endif %}
        </div>
        {% endif %}
    '''
    request = context.get('request')

    get = request.GET.copy()
    get.update(kwargs)

    path = '%s?' % request.path
    for query, val in get.items():
        path += '%s=%s&' % (query, val)

    return path[:-1]

