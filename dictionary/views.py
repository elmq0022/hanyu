'''
Views for the dictionary application.
'''

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SearchForm

def search(request):
    '''
    This is a first crack at a basic search interface.
    '''
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # TODO: Make this do someting.
            return HttpResponseRedirect('some where')
    else:
        form = SearchForm()

    return render(request, 'dictionary/search.html', {'form': form})
