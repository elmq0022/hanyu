from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = '_base.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('accounts:profile'))
        return super().get(request, *args, **kwargs)