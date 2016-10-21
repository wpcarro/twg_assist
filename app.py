#!/usr/bin/env python

import json
import os

from flask import Flask
from flask import request
from flask import make_response

from twg_ops import mine_data
from twg_ops import handle_find
from twg_ops import handle_filter
from twg_ops import handle_download
from twg_ops import handle_show

app = Flask(__name__)


DEBUG = True

supported_actions = {
    'find': handle_find,
    'filter': handle_filter,
    'download': handle_download,
    'show': handle_show
}


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    if DEBUG:
        print('Request:')
        print(json.dumps(req, indent=4))

    res = process_request(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'

    return r


def get_action(req):
    return req.get('result').get('')


def process_request(req):
    params = req.get('result').get('parameters')
    query = params.get('any')

    action = get_action(req)

    data = handle_find(query)
    nugget_text, nugget_url = mine_data(data)

    return curate_webhook_response(nugget_text, nugget_url)


def curate_webhook_response(nugget_text, nugget_url):
    payload = {
        'speech': nugget_text,
        'displayText': nugget_text,
        'data': {
            'slack': nugget_text
        },
        'contextOut': [
            {
                'name': 'nugget',
                'lifespan': 5,
                'parameters': {
                    'nugget_text': nugget_text,
                    'nugget_url': nugget_url
                }
            }
        ],
        "source": 'twg-webhook-processor'
    }

    if DEBUG:
        print('Payload:')
        print(json.dumps(payload, indent=4))

    return payload


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('Starting app on port %d' % port)
    app.run(debug=False, port=port, host='0.0.0.0')
