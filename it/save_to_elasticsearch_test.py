from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from core import process_url
from database import Database

INDEX = 'page'
URL = 'https://news.ycombinator.com/item?id=16195055'


client = Elasticsearch(index='page')


def save_url_to_elasticsearch_test():
    dbargs = {'dbname': 'webparse', 'user': 'webparse_user', 'password': 'pass325', 'host': 'localhost'}
    db = Database(**dbargs)
    pg_page, es_page = process_url(URL, db)
    s = Search(using=client, index=INDEX) \
                      .query('match', _id=es_page.meta.id)

    #s.aggs.bucket('per_tag', 'terms', field='tags')

    response = s.execute()

    assert(len(list(response)) > 0)
