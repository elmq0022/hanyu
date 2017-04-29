from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Word


class WordsView(LoginRequiredMixin, TemplateView):
    template_name = 'learning_tools/learned_status.html'

    def words(self):
        '''
        Return a list of words the user know by the learning status
        attribute.
        '''
        return Word.objects.filter(user=self.request.user).filter(learning_status=self.kwargs['status']).all()

