import urllib.request
import json

keystart = ''

ids = set()

while True:
    print("Ids size is %d" % len(ids))
    r = json.loads(
        urllib.request.urlopen(
            r'http://ifwiki.ru/api.php?action=query&list=categorymembers&'
            r'cmtitle=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:'
            r'%D0%98%D0%B3%D1%80%D1%8B&rawcontinue=1&cmlimit=2000&format=json&'
            r'cmsort=sortkey&cmprop=ids|title|sortkey&'
            r'cmstarthexsortkey=' + keystart).read())
    res = r['query']['categorymembers']

    for x in res:
        ids.add(x['pageid'])

    if len(res) <= 300:
        break
    else:
        keystart = res[-1]['sortkey']


def batch(iterable, n=30):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


total = 0
with open('ifwikiurllist.txt', 'w') as fo:
    for batch in batch(list(ids)):
        pageidlist = '|'.join(["%d" % x for x in batch])
        r = json.loads(
            urllib.request.urlopen(
                r'http://ifwiki.ru/api.php?action=query&prop=info&format=json&'
                r'inprop=url&pageids=' + pageidlist).read())
        for _, v in r['query']['pages'].items():
            total += 1
            fo.write('%s\n' % v['fullurl'])
        print(total)
