import re
from django.core.management.base import BaseCommand
from games.models import *


def IfwikiCapitalizeFile():
    r = re.compile('^(.*ifwiki.ru/files/)(\w)(.*)$')
    for x in URL.objects.all():
        m = r.match(x.original_url)
        if m and m.group(2).islower():
            print(x.original_url)


class Command(BaseCommand):
    help = 'Does some batch processing.'

    def handle(self, *args, **options):
        IfwikiCapitalizeFile()
