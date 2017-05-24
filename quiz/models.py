'''
Models for the quiz application.
'''

import json
import uuid

from django.contrib.auth.admin import User
from django.db import models

from dictionary.models import Entry


class Quiz(models.Model):
    '''
    This model represents a single quiz question.
    The response will be recorded as no-response, incorrect, or correct.
    Results will be stored for the purpose of analysis.
    Both the questions and answers will be represented by foreign keys
    to a dictionary.Entry.
    '''
    user = models.ForeignKey(User)
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField()

    NO_RESPONSE = 'NR'
    INCORRECT = 'IC'
    CORRECT = 'CR'
    RESPONSE = (
        (NO_RESPONSE, 'no response'),
        (INCORRECT, 'incorrect'),
        (CORRECT, 'correct'),
    )

    response = models.CharField(max_length=2, choices=RESPONSE, default=NO_RESPONSE)

    def to_json(self):
        '''
        This function returns a JSON string that will be suitable for use
        in the frontend javascript implementation of the quiz application.
        '''
        quiz_dict = {
            'user_id': self.user.pk,
            'uid': str(self.uid),
            'question': [ans.entry.simple for ans in self.answer_set.all() if ans.correct][0],
            'answers': [{'pk':ans.pk, 'definition':ans.entry.definitions} for ans in self.answer_set.all()]
            }
        return json.dumps(quiz_dict)

    def __str__(self):
        return "user: {} quiz uid: {} reponse: {}".format(self.user.username, self.uid, self.response)


class Answer(models.Model):
    '''
    This model ties the answers back to the quiz.
    '''
    # TODO: uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz)
    entry = models.ForeignKey(Entry)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return "quiz: {} chinese: {} correct: {}".format(self.quiz.uid, self.entry.simple, self.correct)
