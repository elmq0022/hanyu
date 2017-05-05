from django import forms
from .models import WordLearningStatus
from dictionary.models import Entry


class WordStatusUpdateForm(forms.Form):
    words = forms.CharField(widget=forms.Textarea)
    learning_status = forms.CharField()



