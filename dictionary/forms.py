from django import forms


class SearchForm(forms.Form):
    search_text = forms.CharField(label='search', max_length=255)
