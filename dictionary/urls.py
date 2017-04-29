from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'entry/(?P<pk>\d+)/', views.EntryView.as_view(), name='entry'),
    url(r'full_search/', views.FullChineseSearchView.as_view(), name='full_search'),
    url(r'search/', views.SearchView.as_view(), name='search'),
]
