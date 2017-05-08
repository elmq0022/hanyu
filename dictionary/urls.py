from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'entry/(?P<pk>\d+)/', views.EntryView.as_view(), name='entry'),
    url(r'search2/', views.SearchAny.as_view(), name='search2'),
]
