'''
Views for the dictionary application.
'''

import os

import jieba
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import FormView
from nltk.tokenize import stanford_segmenter

from . import forms, models


# class SearchView(FormView):
#     '''
#     This is a full text search of all of the items in a Dictionary Entry.
#     '''
#     template_name = 'dictionary/search.html'

#     def get(self, request, *args, **kwargs):
#         self.results = None
#         form = forms.SearchForm(request.GET or None)
#         if form.is_valid():
#             search_text = form.cleaned_data['search_text']
#             search_vector = SearchVector('simple', 'traditional', 'pin_yin', 'definitions')
#             self.results = (
#                 models.Entry.objects.annotate(search=search_vector).filter(search=search_text))
#             form = forms.SearchForm()
#         return self.render_to_response(self.get_context_data(form=form))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['results'] = self.results
#         return context


# class FullChineseSearchView(FormView):
#     template_name = "dictionary/full_search.html"

#     def get(self, request, *args, **kwargs):
#         self.results = None
#         self.search_terms = None
#         self.search_text = None
#         form = forms.SearchForm(request.GET or None)
#         if form.is_valid():
#             self.search_text = form.cleaned_data['search_text']
#             self.search_terms = jieba.cut(self.search_text)
#             # self.results = {} 
#             self.results = [] 

#             for search_term in self.search_terms:
#                 entry = models.Entry.objects.filter(simple=search_term)
#                 if entry:
#                     # self.results[search_term] = entry
#                     self.results.append((search_term, entry))
#                 else:
#                     for character in search_term:
#                         # self.results[character] = models.Entry.objects.filter(simple=character)
#                         self.results.append((character,
#                                              models.Entry.objects.filter(simple=character)))
#             form = forms.SearchForm()

#         return self.render_to_response(self.get_context_data(form=form))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['search_terms'] = self.search_terms
#         context['results'] = self.results
#         context['searched'] = self.search_text
#         return context


class EntryView(TemplateView):
    template_name = 'dictionary/entry.html'

    def entry(self):
        return models.Entry.objects.get(pk=self.kwargs['pk'])

    def top_related(self):
        return 'RELATED' # TODO: Fix this!

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entry'] = self.entry()
        context['top_related'] = self.top_related()
        return context


class SearchAny(TemplateView):
    template_name = 'dictionary/search2.html'
    model = models.Entry

    def word_search(self, search_text):
        '''
        Does a full text search of the exact term entered.
        '''
        search_vector = SearchVector('simple', 'traditional', 'pin_yin', 'definitions')
        return models.Entry.objects.annotate(search=search_vector).filter(search=search_text)

    def segemented_search(self, search_text):
        '''
        Segments the entered search term and return an entry for each result.
        '''
        search_terms = jieba.cut(search_text)
        results = []
        for search_term in search_terms:
            entry = models.Entry.objects.filter(simple=search_term)
            if entry:
                results.append((search_term, entry))
            else:
                for character in search_term:
                    results.append((character, models.Entry.objects.filter(simple=character)))
        return results

    def get_entry_list(self):
        self.searched = self.request.GET.get('search_text')
        self.search_type = self.request.GET.get('search_type')

        if self.search_type == '0':
            qs = self.word_search(self.searched)
        elif self.search_type == '1':
            import pdb
            qs = self.segemented_search(self.searched)
        else:
            qs = []
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context['entry_list'] = self.get_entry_list()
        context['searched'] = self.searched
        context['search_type'] = self.search_type
        return context
