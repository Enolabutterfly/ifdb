from django.conf import settings
from django.urls import include, re_path
from django_registration.backends.activation.views import RegistrationView

from core.forms import RegistrationForm

from . import views

urlpatterns = [
    re_path(r"^index/$", views.index, name="index"),
    # Games
    re_path(r"^game/add/", views.add_game, name="add_game"),
    re_path(
        r"^game/edit/(?P<game_id>\d+)/", views.edit_game, name="edit_game"
    ),
    re_path(r"^game/vote/", views.vote_game, name="vote_game"),
    re_path(r"^game/store/", views.store_game, name="store_game"),
    re_path(r"^game/comment/", views.comment_game, name="comment_game"),
    re_path(r"^game/search/", views.search_game, name="search_game"),
    re_path(r"^game/$", views.list_games, name="list_games"),
    re_path(r"^game/(?P<game_id>\d+)/", views.show_game, name="show_game"),
    re_path(
        r"^game/interpreter/(?P<gameurl_id>\d+)/store/",
        views.store_interpreter_params,
        name="store_interpreter_params",
    ),
    re_path(
        r"^game/interpreter/(?P<gameurl_id>\d+)/",
        views.play_in_interpreter,
        name="play_in_interpreter",
    ),
    # Authors
    re_path(r"^author/$", views.list_authors, name="list_authors"),
    re_path(
        r"^author/(?P<author_id>\d+)/", views.show_author, name="show_author"
    ),
    # API
    re_path(r"^json/gameinfo/", views.json_gameinfo, name="json_gameinfo"),
    re_path(
        r"^json/commentvote/", views.json_commentvote, name="json_commentvote"
    ),
    re_path(
        r"^json/categorizeurl/",
        views.json_categorizeurl,
        name="json_categorizeurl",
    ),
    re_path(r"^json/upload/", views.upload, name="upload"),
    re_path(r"^json/import/", views.doImport, name="import"),
    re_path(r"^json/search/", views.json_search, name="json_search"),
    re_path(
        r"^json/author-search/",
        views.json_author_search,
        name="json_author_search",
    ),
    re_path(
        r"^accounts/register/$",
        RegistrationView.as_view(form_class=RegistrationForm),
        name="registration_register",
    ),
    re_path(
        r"^accounts/",
        include(
            "django_registration.backends.activation.urls"
            if settings.REQUIRE_ACCOUNT_ACTIVATION
            else "django_registration.backends.one_step.urls"
        ),
    ),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
