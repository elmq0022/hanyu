'''
Views for the dictionary application.
'''

import os

import jieba
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

import dictionary
import learning_tools
from learning_tools import forms


class EntryView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'dictionary/entry.html'
    model = learning_tools.models.WordLearningStatus
    fields = ['learning_status', ]
    success_message = "Updated Learning Status"

    def get_success_url(self):
        return self.entry.get_absolute_url()

    def get_object(self, queryset=None):
        user = self.request.user
        self.entry = dictionary.models.Entry.objects.get(pk=self.kwargs['pk'])
        obj = learning_tools.models.WordLearningStatus.objects.filter(Q(user=user) & Q(entry=self.entry)).first()
        if obj:
            return obj
        else:
            obj = learning_tools.models.WordLearningStatus(user=user, entry=self.entry)
            obj.save()
        return obj

    def top_related(self):
        return 'RELATED' # TODO: Fix this!

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entry'] = dictionary.models.Entry.objects.get(pk=self.kwargs['pk'])
        context['top_related'] = self.top_related()
        return context


class SearchAny(ListView):
    template_name = 'dictionary/search.html'
    context_object_name = 'entry_list'
    model = dictionary.models.Entry

    def word_search(self, search_text):
        '''
        Does a full text search of the exact term entered.
        '''
        search_vector = SearchVector('simple', 'traditional', 'pin_yin', 'definitions')
        return dictionary.models.Entry.objects.annotate(search=search_vector).filter(search=search_text)

    def segemented_search(self, search_text):
        '''
        Segments the entered search term and return an entry for each result.
        '''
        search_terms = jieba.cut(search_text)
        results = []
        for search_term in search_terms:
            entry = dictionary.models.Entry.objects.filter(simple=search_term)
            if entry:
                results.append((search_term, entry))
            else:
                for character in search_term:
                    results.append((character, dictionary.models.Entry.objects.filter(simple=character)))
        return results

    def get_queryset(self):
        self.searched = self.request.GET.get('search_text')
        self.search_type = self.request.GET.get('search_type')

        if self.search_type == '0':
            qs = self.word_search(self.searched)
        elif self.search_type == '1':
            qs = self.segemented_search(self.searched)
        else:
            qs = []
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context['searched'] = self.searched
        context['search_type'] = self.search_type
        return context
