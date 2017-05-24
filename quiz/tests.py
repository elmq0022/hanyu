from django.test import TestCase
from django.contrib.auth.admin import User

from .views import create_quiz
import pytest


# Create your tests here.
@pytest.mark.django_db
def test_create_quiz():
    User.objects.create_user(username="test_user")
    assert User.objects.all().count() == 1

