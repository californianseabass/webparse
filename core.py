import bs4
import elasticsearch
import elasticsearch_dsl
import hashlib
import inspect
import mmh3
import re
import requests


from database import Database
from es import Page


def generate_url_hash(url):
    url_hash = hashlib.sha256()
    url_hash.update(url.encode('utf-8'))
    hash_str = url_hash.hexdigest()
    print(hash_str)
    return hash_str


def clean_title_string(title):
    return re.sub('\s+', ' ', title.strip())


def parse_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        title = clean_title_string(soup.title.string)
        text = soup.get_text()
        return title, text
    else:
        response.raise_for_status()
        return None, None


def search_pages(search_term):
    client = elasticsearch.Elasticsearch()
    search = elasticsearch_dsl.Search(using=client, index='page') \
                              .query('match', body=search_term)
    response = search.execute()
    return [
        {
            'tags': hit.tags,
            'title': hit.title,
            'url': hit.url
        } for hit in response.hits
    ]


def process_url(url, db_object):
    """ Uses an underlying library to scrape a webpage, and then creates an object
        that is appropriate for storage in elasticsearch

        Args:
            url (str): string repr of a url
            tags (list[str]): a list of user generated tags associated with the url

        Returns:
            Page: Instance of an es-Doctype subclass, represents information for page

    """
    if not inspect.isclass(Database):
        raise Exception('db_object must be of class Database')
    hash_id = generate_url_hash(url)
    title, orig_text = parse_url(url)
    if not title or not orig_text:
        print(f'failed to save:{url}')
        return
    pg_page = db_object.save_url_to_table(url)
    es_page = None
    if pg_page:
        text = ' '.join(orig_text.split())
        #hash_id = mmh3.hash(text)  # murmur hash, 32 bit
        es_page = Page(meta={'id': hash_id}, url=url, title=title, body=text, tags='')
        es_page.save()
    else:
        client = elasticsearch.Elasticsearch(index='page')
        search = elasticsearch_dsl.Search().using(client).query('match', _id=hash_id)
        try:
            es_page = search.execute()[0]
        except IndexError as ie:
            print('Elasticsearch is missing something that postgres has')

    return (pg_page, es_page)


def process_urls(urls):
    pages = list(map(process_url, urls))
    ids = [x._id for x in pages]
    print(ids)
