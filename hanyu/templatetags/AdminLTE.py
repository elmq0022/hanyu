from hashlib import md5

from django import template
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()


@register.inclusion_tag('_menu_tree_open.html', takes_context=True)
def menu_tree_open(context, heading):
    '''
    heading         := Menu heading
    descriptions    := list of sub-menu link descriptions
    urls            := list of sub-menu urls
    args            := list of tuples of keyword, argument pairs [((k,a),..., (k,a)),..., ((k,a),...) ]
    '''
    context['heading'] = heading
    return context


@register.inclusion_tag('_menu_tree_item.html', takes_context=True)
def menu_tree_item(context, url_namespace, description, *args):
    '''
    description    := list of sub-menu link descriptions
    url            := list of sub-menu urls
    '''
    extra = {a: b for a, b in zip(args[0::2], args[1::2])} if args else None
    link = reverse(url_namespace, kwargs=extra)
    context['description'] = description
    context['link'] = link
    return context


@register.inclusion_tag('_menu_tree_close.html', takes_context=True)
def menu_tree_close(context):
    return context


@register.simple_tag(takes_context=True)
def gravitar(context, **kwargs):
    '''
    Link to a user's gravatar based on their supplied email.
    '''
    html = r'<img src="https://www.gravatar.com/avatar/{}?d={}"?s={}/ class="{}" alt="User Image">'
    image_id = '00000000000000000000000000000000'
    image_size = kwargs.get('size', 20)
    image_default = kwargs.get('default', '')
    image_class = kwargs.get('class', 'img-circle')
    user = context['user']
    if user.is_authenticated:
        image_id = md5(user.email.encode('utf-8')).hexdigest()
    return format_html(html, image_id, image_default, image_size, image_class)
