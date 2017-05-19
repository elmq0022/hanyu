'''
Models for the quiz application.
'''

from django.contrib.auth.admin import User
from django.db import models

from dictionary.models import Entry


class Quiz(models.Model):
    '''
    This model represents a single quiz question.
    The response will be recorded as no response, incorrect, or correct.
    Results will be stored for the purpose of analysis.
    Both the questions and answers will be represented by foreign keys
    to a dictionary.Entry.
    '''
    user = models.ForeignKey(User)
    uid = models.UUIDField(primary_key=True)
    question = models.ForeignKey(Entry)
    answer = models.ForeignKey(Entry)
    date = models.DateTimeField()

    NO_RESPONSE = 'N'
    INCORRECT = 'I'
    CORRECT = 'C'
    RESPONSE = (
        (NO_RESPONSE, 'no response'),
        (INCORRECT, 'incorrect'),
        (CORRECT, 'correct'),
    )

    response = models.CharField(max_length=1, choices=RESPONSE, default=NO_RESPONSE)
