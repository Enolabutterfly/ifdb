from .models import GameAuthorRole, Author
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


def index(request):
    return render(request, 'games/index.html', {})


@ensure_csrf_cookie
def add_game(request):
    return render(request, 'games/add.html', {})

########################
# Json handlers below. #
########################


def authors(request):
    res = {'roles': [], 'authors': [], 'value': []}
    for x in GameAuthorRole.objects.order_by('order', 'title').all():
        res['roles'].append({'title': x.title, 'id': x.id})

    for x in Author.objects.order_by('name').all():
        res['authors'].append({'name': x.name, 'id': x.id})

    for x in range(1, 3):
        res['value'].append({'author': x, 'role': x})

    return JsonResponse(res)
