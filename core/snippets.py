from .models import Snippet
from django.template.loader import render_to_string
from django.utils import timezone
from games.models import GameURL
from games.search import MakeSearch
from games.tools import FormatLag
from django.urls import reverse
import json


def GameListFromSearch(request, query, reltime_field=None):
    s = MakeSearch(request.perm)
    s.UpdateFromQuery(query)
    games = s.Search(
        prefetch_related=['gameauthor_set__author', 'gameauthor_set__role'],
        start=0,
        limit=20)[:5]

    posters = (GameURL.objects.filter(category__symbolic_id='poster').filter(
        game__in=games).select_related('url'))

    g2p = {}
    for x in posters:
        g2p[x.game_id] = x.GetLocalUrl()

    for x in games:
        x.poster = g2p.get(x.id)
        x.authors = [
            x for x in x.gameauthor_set.all() if x.role.symbolic_id == 'author'
        ]

    if reltime_field:
        for x in games:
            x.lag = FormatLag(
                (getattr(x, reltime_field) - timezone.now()).total_seconds())
    return games


def GameListSnippet(request, query, reltime_field=None):
    games = GameListFromSearch(request, query, reltime_field)
    items = []
    for x in games:
        lines = []
        if hasattr(x, 'lag'):
            lines.append({'style': 'comment', 'text': x.lag})
        lines.append({'style': 'strong', 'text': x.title})
        lines.append({'text': ', '.join([y.author.name for y in x.authors])})
        items.append({
            'image': x.poster or '/static/noposter.png',
            'lines': lines,
            'link': reverse('show_game', kwargs={
                'game_id': x.id
            }),
        })
    return render_to_string('core/snippet.html', {'items': items})


def RenderSnippets(request):
    snippets = []
    now = timezone.now()
    for x in Snippet.objects.order_by('order'):
        if not request.perm(x.view_perm):
            continue
        if x.show_start and x.show_start > now:
            continue
        if x.show_end and x.show_end < now:
            continue
        style = json.loads(x.style_json)
        content_json = json.loads(x.content_json)

        box_style = "grid-box-%s" % style['color'] if 'color' in style else ''

        if 'method' in content_json:
            method = content_json['method']
            del content_json['method']
            content = globals()[method](request, **content_json)
        else:
            content = ''

        snippets.append({
            'title': x.title,
            'box_style': box_style,
            'content': content,
        })

    return render_to_string('core/snippets.html', {'snippets': snippets})