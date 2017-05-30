
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'words/(?P<status>UN|AC|LN)/$', views.WordStatusView.as_view(), name='word_status'),
    url(r'update_word_status/$', views.WordStatusUpdateView.as_view(), name='update_word_status'),
]
