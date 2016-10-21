import json
import random
import urllib


def mine_data(data):
    nuggets = data.get('text')
    urls = data.get('urls')

    rand_index = random.randint(0, len(nuggets))

    return nuggets[rand_index], urls[rand_index]


def handle_filter(req):
    criterion = req.get('result')

    print('filtering by criterion: %s' % criterion)


def handle_find(req):
    print('handle_find')

    query = req.get('result').get('parameters').get('any')

    print('query: %s' % query)

    base_url = 'https://huge-echo.appspot.com/_ah/api/twg_api/v1/query?query='
    twg_query = base_url + query
    res = urllib.request.urlopen(twg_query).read()

    parsed_json = json.loads(str(res, 'utf-8'))
    nugget_text, nugget_url = mine_data(parsed_json)

    return nugget_text


def handle_download(req):
    pass


def handle_show(req):
    pass
