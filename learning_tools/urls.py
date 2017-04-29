
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'words/(?P<status>UN|AC|LN)/', views.WordsView.as_view(), name='words'),
]
