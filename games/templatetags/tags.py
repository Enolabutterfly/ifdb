import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def current(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return mark_safe('class="current"')
    return ''
