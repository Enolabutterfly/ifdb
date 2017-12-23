from django.utils import timezone
from .models import FeedCache, RssFeedsToCache
import feedparser
from time import mktime
from datetime import datetime
from logging import getLogger

logger = getLogger('worker')


def FetchFeed(url, feed_id):
    logger.info("Fetching feed at %s" % url)
    feed = feedparser.parse(url)
    now = timezone.now()
    for x in feed.entries:
        try:
            f = FeedCache.objects.get(feed_id=feed_id, item_id=x.id)
        except FeedCache.DoesNotExist:
            f = FeedCache()
            f.feed_id = feed_id
            f.item_id = x.id
            f.date_discovered = now
        f.date_published = datetime.fromtimestamp(mktime(x.published_parsed))
        f.title = x.title
        f.authors = x.author
        f.url = x.link
        f.save()


def FetchFeeds():
    for x in RssFeedsToCache.objects.all():
        FetchFeed(x.rss_url, x.feed_id)
