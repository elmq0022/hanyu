from pdb import set_trace
from django import template 
from django.utils.html import format_html, format_html_join
from django.conf import settings

register = template.Library()

@register.inclusion_tag('_menu_tree.html', takes_context=True)
def menu_tree(context):
    context['menu'] = settings.SITE_MENU
    print(context)
    return context
