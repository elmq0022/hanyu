'''
Views for the dictionary application.
'''

import os

from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.views.generic.edit import FormView
from nltk.tokenize import stanford_segmenter

from . import forms, models


class SearchView(FormView):
    '''
    This is a full text search of all of the items in a Dictionary Entry.
    '''
    template_name = 'dictionary/search.html'

    def get(self, request, *args, **kwargs):
        self.results = None
        form = forms.SearchForm(request.GET or None)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            search_vector = SearchVector('simple', 'traditional', 'pin_yin', 'definitions')
            self.results = (
                models.Entry.objects.annotate(search=search_vector).filter(search=search_text))
            form = forms.SearchForm()
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = self.results
        return context


class FullChineseSearchView(FormView):
    template_name = "dictionary/full_search.html"

    def __init__(self):

        os.environ['JAVAHOME'] = settings.JAVAHOME
        os.environ['CLASSPATH'] = settings.CLASSPATH
        self.segmenter = stanford_segmenter.StanfordSegmenter(
            path_to_jar=settings.STFD_SEG,
            path_to_slf4j=settings.SLF4J,
            path_to_sihan_corpora_dict=settings.SIHAN_DICT,
            path_to_model=settings.MODEL,
            path_to_dict=settings.DICT
            )
        super().__init__()

    def get(self, request, *args, **kwargs):
        self.results = None
        self.search_terms = None
        self.search_text = None
        form = forms.SearchForm(request.GET or None)
        if form.is_valid():
            self.search_text = form.cleaned_data['search_text']
            self.search_terms = self.segmenter.segment(self.search_text).split()
            self.results = {} 

            for search_term in self.search_terms:
                self.results[search_term] = \
                    models.Entry.objects.filter(simple=search_term)

            form = forms.SearchForm()
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_terms'] = self.search_terms
        context['results'] = self.results
        context['searched'] = self.search_text
        return context
