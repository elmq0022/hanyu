from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import TemplateView

from analysis.models import Count

from . import forms


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/login.html'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class SignUpView(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/home.html'

    def get_top_characters(self):
        return Count.objects.filter(count_type=Count.CHARACTER).all().order_by('-count')[:5] 

    def get_top_words(self):
        return Count.objects.filter(count_type=Count.WORD).all().order_by('-count')[:5] 

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_characters = self.get_top_characters()
        top_words = self.get_top_words()
        context['top_characters'] = top_characters
        context['top_words'] = top_words
        return context
        