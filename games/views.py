from .models import GameTagCategory, Author
from django.http.response import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, 'games/index.html', {})


def add_game(request):
    return render(request, 'games/add.html', {})


def authors(request):
    res = {'categories': [], 'authors': []}
    for x in GameTagCategory.objects.order_by('order', 'name').all():
        res['categories'].append({'name': x.name, 'id': x.id})

    for x in Author.objects.order_by('name').all():
        res['authors'].append({'name': x.name, 'id': x.id})

    return JsonResponse(res)
