from django import forms


class QuizForm(forms.Form):
    text_field = forms.Textarea()
    CHOICES = [('select1', 'select1'),
               ('select2', 'select2'),]
    radio = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    question = forms.Textarea()