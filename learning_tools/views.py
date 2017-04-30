from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import WordLearningStatus


class WordStatusView(LoginRequiredMixin, TemplateView):
    template_name = 'learning_tools/learning_status.html'

    def word_learning_status(self):
        '''
        Return a list of words the user know by the learning status
        attribute.
        '''
        return WordLearningStatus.objects.filter(user=self.request.user).filter(learning_status=self.kwargs['status']).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['word_learning_status'] = self.word_learning_status()
        return context
