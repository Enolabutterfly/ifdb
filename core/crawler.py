from django.conf import settings
import datetime
import hashlib
import urllib.request
import json
import os.path
from urllib.parse import quote

def FetchUrlToString(url):
    print('Fetching: %s' % url)
    filename_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    if settings.CRAWLER_CACHE_DIR:
        filename = os.path.join(settings.CRAWLER_CACHE_DIR, filename_hash)
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                return f.read().decode('utf-8')

    url = quote(url.encode('utf-8'), safe='/+=&?%:@;!#$*()_-')
    with urllib.request.urlopen(url) as response:
        contents = response.read()
        if settings.CRAWLER_CACHE_DIR:
            filename = os.path.join(settings.CRAWLER_CACHE_DIR, filename_hash)
            with open(filename, 'wb') as f:
                f.write(contents)
            with open(filename + '.meta', 'w') as f:
                metadata = {
                    'url': url,
                    'time': str(datetime.datetime.now()),
                    'filename': response.info().get_filename(),
                    'content-type': response.info().get_content_type(),
                }
                f.write(json.dumps(metadata, indent=2, separators=(',', ': ')))
        return contents.decode('utf-8')