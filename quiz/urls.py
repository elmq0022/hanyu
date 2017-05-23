from django.conf.urls import url

from . import views

urlpatterns =[
    url(r'quiz/$', views.QuizView.as_view(), name='quiz'),
    url(r'json/$', views.QuizJSON.as_view(), name='json'),
    url(r'answer/$', views.answer_question, name='answer'),
]