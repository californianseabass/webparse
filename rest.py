#!/usr/bin/env python
import json
import requests
from flask import Flask, Response, jsonify, request

from core import process_url
from database import Database, DB_ARGS


API_VERSION = 0.1
BASENAME = f'/webparse/api/v{API_VERSION}/'

app = Flask(__name__)
dbargs = {
    'dbname': 'webparse',
    'user': 'webparse_user',
    'password': 'pass325',
    'host': 'localhost'
}
db = Database(**DB_ARGS)


@app.route('/')
def index():
    return Response(open('index.html').read(), mimetype='html')


@app.route('/url/<uid>')
def url_by_uid(uid):
    """ curl -H "Content-Type: application/json" -X GET http://localhost:5000/url/hash_id
    """
    url = db.get_url_by_md5_hash(uid)
    response = requests.get(url[0])
    return Response(response.content.decode('utf-8'), mimetype='html')


@app.route('/webparse/api/v0.1/pages', methods=['GET', 'POST'])
def page():
    """ curl -H "Content-Type: application/json" -X POST -d '{"url":"https://news.ycombinator.com/item?id=16406761"}' http://localhost:5000/webparse/api/v0.1/pages
    """
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf8'))
        pg_page, es_page = process_url(data['url'], db)
        return jsonify({
            'url': pg_page[1],
            'md5_hash': pg_page[2]
        })


if __name__ == '__main__':
    app.run(debug=True)
