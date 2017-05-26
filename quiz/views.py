import json
import random
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from dictionary.models import Entry
from learning_tools.models import WordLearningStatus as WLS

from .json_response_mixin import JSONResponseMixin
from .models import Answer, Quiz


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
        return HttpResponse(json.dumps(data), content_type="application/json")
    if request.method == "GET":
        q = Quiz.objects.get(pk="9279f903-aa86-47f1-b313-82da028dd0e0")
        return HttpResponse(q.to_json(), content_type="application/json")


def create_quiz(user, num_answers=6):
    quiz = Quiz(user=user,
                date=datetime.now(),
                response=Quiz.NO_RESPONSE,
               )
    quiz.save()

    count = WLS.objects.filter(
        Q(user=user),
        Q(learning_status=WLS.ACQUIRING) | Q(learning_status=WLS.LEARNED)).count()


    word_query_set = WLS.objects.filter(
        Q(user=user),
        Q(learning_status=WLS.ACQUIRING) | Q(learning_status=WLS.LEARNED))

    samples = random.sample(range(0, count), num_answers)
    words = [word_query_set[sample] for sample in samples]

    correct = random.randint(0, num_answers-1)
    for i, word in enumerate(words):
        Answer(quiz=quiz,
               entry=word.entry,
               correct=(i == correct)
              ).save()


# Consider using a class based view with a form later.
# Right now just get the above working.
# class QuizJSON(JSONResponseMixin, TemplateView):
#     '''
#     This view will serve the quiz as a JSON object.
#     '''
#     def render_to_response(self, context, **kwargs):
#         return self.render_to_json_response(context, **kwargs)
#
#     def get_data(self, context):
#         q = Quiz.objects.get(pk="9279f903-aa86-47f1-b313-82da028dd0e0")
#         context = json.loads(q.to_json())
#         return context
