from hashlib import md5

from django import template
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()


@register.inclusion_tag('_menu_tree.html', takes_context=True)
def menu_tree(context, heading, *args):
    '''
    This is a tag used to build the AdminLTE 2 tree menu
    The first argument is the menu heading.
    The following arguments are alternating namespace:urls and the description
    '''
    links = []
    for url, desc in zip(args[0::2], args[1::2]):
        links.append({'url':reverse(url), 'desc':desc})

    context['heading'] = heading
    context['links'] = links
    return context


@register.simple_tag(takes_context=True)
def gravitar(context, **kwargs):
    html = r'<img src="https://www.gravatar.com/avatar/{}?d={}"?s={}/ class="{}" alt="User Image">'
    image_id = '00000000000000000000000000000000'
    image_size = kwargs.get('size', 20)
    image_default = kwargs.get('default', '')
    image_class = kwargs.get('class', 'img-circle')
    user = context['user']
    if user.is_authenticated:
        image_id = md5(user.email.encode('utf-8')).hexdigest()
    return format_html(html, image_id, image_default, image_size, image_class)
