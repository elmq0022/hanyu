from random import randint

from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import Quiz


class QuizView(TemplateView):
    template_name = 'quiz/quiz.html'

    def get_random_quiz(self):
        count = Quiz.objects.all().count()
        return count

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_random_quiz()
        return context

