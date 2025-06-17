from django.urls import re_path

from moder.actions.tools import HandleAction

urlpatterns = [
    re_path(r"^json/action/$", HandleAction, name="handle_action"),
]
