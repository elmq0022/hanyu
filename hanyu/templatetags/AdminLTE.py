from django import template 
from django.core.urlresolvers import reverse

register = template.Library()


@register.inclusion_tag('_menu_tree.html', takes_context=True)
def menu_tree(context, heading, *args):
    '''
    This is a tag used to build the AdminLTE 2 tree menu
    The first argument is the menu heading.
    The following arguments are alternating namespace:urls and the description
    '''

    links = []
    from pdb import set_trace
    set_trace()
    for url, desc in zip(args[0::2], args[1::2]):
        links.append({'url':reverse(url), 'desc':desc})

    context['heading'] = heading
    context['links'] = links
    return context
