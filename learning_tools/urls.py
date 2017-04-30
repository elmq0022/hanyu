
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'words/(?P<status>UN|AC|LN)/', views.WordStatusView.as_view(), name='word_status'),
]
