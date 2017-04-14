'''
Views for the dictionary application.
'''

from django.contrib.postgres.search import SearchVector
from django.views.generic.edit import FormView

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
