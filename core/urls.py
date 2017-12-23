from django.conf.urls import url
from . import views, snippets

urlpatterns = [
    url(r'^api/v0/fetchpackage$', views.fetchpackage, name='fetchpackage'),
    url(r'^api/v0/logtime$', views.logtime, name='logtime'),
    url(r'^json/snippet/', snippets.AsyncSnippet, name='async_snippet'),
    url(r'^docs/(?P<slug>[-\w]+)', views.showdoc, name='showdoc'),
]
