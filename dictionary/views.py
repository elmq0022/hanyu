'''
Views for the dictionary application.
'''

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.postgres.search import SearchVector

from . import forms
from . import models

def search(request):
    '''
    This is a first crack at a basic search interface.
    '''
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            search_vector = SearchVector('simple', 'traditional', 'pin_yin', 'definitions')
            results = models.Entry.objects.annotate(search=search_vector).filter(search=search_text)
            form = forms.SearchForm()
            return render(request, 'dictionary/search.html', {'form': form, 'results': results,})
    else:
        form = forms.SearchForm()

    return render(request, 'dictionary/search.html', {'form': form})
