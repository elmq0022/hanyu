from random import randint, sample

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from .json_response_mixin import JSONResponseMixin
import json


from .models import Quiz


class QuizView(TemplateView):
    '''
    Serve the template for quiz application.
    This is need simply to extend the _base.html template
    and to include the CSRF token.
    '''
    template_name = 'quiz/quiz.html'

    def get_random_quiz(self):
        count = Quiz.objects.all().count()
        return count

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_random_quiz()
        return context


class QuizJSON(JSONResponseMixin, TemplateView):
    '''
    This view will serve the quiz as a JSON object.
    '''
    def render_to_response(self, context, **kwargs):
        return self.render_to_json_response(context, **kwargs)
 
    def get_data(self, context):
        q = Quiz.objects.get(pk="9279f903-aa86-47f1-b313-82da028dd0e0")
        context = q.to_json()
        return context


def answer_question(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
