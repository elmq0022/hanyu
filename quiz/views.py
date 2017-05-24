import json
from random import randint, sample

from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .json_response_mixin import JSONResponseMixin
from .models import Answer
from .models import Quiz


class QuizView(TemplateView):
    '''
    Serve the template for quiz application.
    This is need simply to extend the _base.html template
    and to include the CSRF token.
    '''
    template_name = 'quiz/quiz.html'


def answer_question(request):
    if request.method == "POST":
        data = request.POST
        uid = data['uid']
        q = Quiz.objects.get(uid=uid)
        a = Answer.objects.get(pk=data['answer_pk'])
        print(q, a)
        return HttpResponse(json.dumps(data), content_type="application/json")
    if request.method == "GET":
        q = Quiz.objects.get(pk="9279f903-aa86-47f1-b313-82da028dd0e0")
        return HttpResponse(q.to_json(), content_type="application/json")


# Consider using a class based view with a form later.
# Right now get just get the above working.
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
