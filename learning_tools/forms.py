from django import forms
from .models import WordLearningStatus
from dictionary.models import Entry


class WordStatusUpdateForm(forms.Form):
    UNLEARNED = 'UN'
    ACQUIRING = 'AC'
    LEARNED = 'LN'
    LEARNING_STATUS = (
        (UNLEARNED, 'unlearned'),
        (ACQUIRING, 'acquiring'),
        (LEARNED, 'learned'),
    )

    words = forms.CharField(widget=forms.Textarea)
    learning_status = forms.ChoiceField(required=True, choices=(LEARNING_STATUS))
