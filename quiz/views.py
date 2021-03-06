import json
import random
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


from dictionary.models import Entry
from learning_tools.models import WordLearningStatus as WLS

from .json_response_mixin import JSONResponseMixin
from .models import Answer, Quiz


class QuizView(LoginRequiredMixin, TemplateView):
    '''
    Serve the template for quiz application.
    This is need simply to extend the _base.html template
    and to include the CSRF token.
    '''
    template_name = 'quiz/quiz.html'


@login_required() # This seems to work without specifying the redirect.  Probably because I used the django defaults.
def quiz_data(request):
    if request.method == "POST":
        data = request.POST
        uid = data['uid']
        quiz = Quiz.objects.get(uid=uid)
        answers = quiz.answer_set.all()
        correct_answer = answers.filter(correct=True).all()[0]
        quiz.response = Quiz.CORRECT if correct_answer.pk == data['answer_pk'] else Quiz.INCORRECT
        quiz.save()
        result = {'correct_pk': correct_answer.pk}
        return HttpResponse(json.dumps(result), content_type="application/json")

    else:
        quiz = create_quiz(request.user, 3)
        return HttpResponse(quiz.to_json(), content_type="application/json")


def create_quiz(user, num_answers=6):
    quiz = Quiz(user=user,
                date=datetime.now(),
                response=Quiz.NO_RESPONSE,
               )
    quiz.save()

    count = WLS.objects.filter(Q(user=user),
                               Q(learning_status=WLS.ACQUIRING) |
                               Q(learning_status=WLS.LEARNED)
                              ).count()

    num_answers = min(num_answers, count)

    word_query_set = WLS.objects.filter(
        Q(user=user),
        Q(learning_status=WLS.ACQUIRING) | Q(learning_status=WLS.LEARNED))

    samples = random.sample(range(0, count), num_answers)
    words = [word_query_set[sample] for sample in samples]

    correct = random.randint(0, num_answers-1)
    for i, word in enumerate(words):
        Answer(quiz=quiz, entry=word.entry, correct=(i == correct)).save()

    return quiz

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
