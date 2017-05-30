from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from dictionary.models import Entry

from .forms import WordStatusUpdateForm
from .models import WordLearningStatus


class WordStatusView(LoginRequiredMixin, TemplateView):
    template_name = 'learning_tools/learning_status.html'

    def word_learning_status(self):
        '''
        Return a list of words the user knows by the learning status
        attribute.
        '''
        return WordLearningStatus.objects.filter(user=self.request.user).filter(learning_status=self.kwargs['status']).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['word_learning_status'] = self.word_learning_status()
        return context


class WordStatusUpdateView(FormView):
    template_name = 'learning_tools/word_status_update.html'
    form_class = WordStatusUpdateForm
    success_url = reverse_lazy('learning:update_word_status')

    def form_valid(self, form):
        words = form.cleaned_data['words']
        learning_status = form.cleaned_data['learning_status']
        user = self.request.user
        for word in words.split():
            entry = Entry.objects.filter(simple=word).all()[0]
            WordLearningStatus.objects.update_or_create(entry=entry,
                                                        user=user,
                                                        defaults={'learning_status': learning_status}
                                                       )
        return super().form_valid(form)
