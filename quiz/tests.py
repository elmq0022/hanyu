import os

import pytest
from django.contrib.auth.admin import User
from django.test import TestCase

from dictionary.management.commands import load_cedict
from dictionary.models import Entry
from hanyu.settings_dev import BASE_DIR  # Fix this so it's right.
from learning_tools.models import WordLearningStatus
from quiz.models import Answer, Quiz

from .views import create_quiz


class CreateTestEntries(load_cedict.Command):
    def download_dict(self):
        '''
        Overload to return data from a local static file for testing purposes.
        This is a smaller set of static data.
        '''
        with open(os.path.join(BASE_DIR, "hanyu", "resources", "min_cedict.txt"), encoding="utf8") as f:
            data = f.read()
        return data


def make_word_status(user, entries, status):
    for e in entries:
        w = WordLearningStatus(
           entry = e,
           user = user,
           learning_status = status 
        )
        w.save()


def setup_db():
    '''
    Setup a small test database for testing.
    '''

    # Create a couple test users
    User.objects.create_user(username="test_user_one")
    User.objects.create_user(username="test_user_two")
    user_one = User.objects.get(username="test_user_one")
    user_two = User.objects.get(username="test_user_two")

    # Load some entries to the entry database
    load = CreateTestEntries()
    load.handle()

    # For each user give them some entries in the acquiring and learned states
    entries_user_one = Entry.objects.all()[:20]
    entries_user_two = Entry.objects.all()[20:40]
    make_word_status(user_one, entries_user_one[:10], WordLearningStatus.ACQUIRING)
    make_word_status(user_one, entries_user_one[10:20], WordLearningStatus.LEARNED)
    make_word_status(user_two, entries_user_one[20:30], WordLearningStatus.ACQUIRING)
    make_word_status(user_two, entries_user_one[30:40], WordLearningStatus.LEARNED)


# Create your tests here.
@pytest.mark.django_db
def test_create_quiz():
    setup_db()
    assert User.objects.all().count() == 2
