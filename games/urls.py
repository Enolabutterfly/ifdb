from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^add/', views.add_game, name='add_game'),
    url(r'^json/authors/', views.authors, name='authors'),
]
