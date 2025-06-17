from django.urls import re_path

from . import editor, views

urlpatterns = [
    re_path(r"^$", views.list_competitions, name="list_competitions"),
    re_path(
        r"^showvotes/(?P<id>\d+)/$", views.list_votes, name="view_compvotes"
    ),
    re_path(
        r"^edit/(?P<id>\d+)/$",
        editor.edit_competition,
        name="edit_competition",
    ),
    re_path(
        r"^editlist/(?P<id>\d+)/$", editor.edit_complist, name="edit_complist"
    ),
    re_path(
        r"^editdoc/(?P<id>\d+)/$", editor.edit_compdoc, name="edit_compdoc"
    ),
    re_path(
        r"^(?P<slug>[-\w\d]+)/(?P<doc>.*)$",
        views.show_competition,
        name="show_competition",
    ),
]
