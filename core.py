import bs4
import mmh3
import requests
import psycopg2
import pprint
import uuid


from es import Page


def parse_url(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    return text


def process_url(url):
    """ Uses an underlying library to scrape a webpage, and then creates an object
        that is appropriate for storage in elasticsearch

        Args:
            url (str): string repr of a url
            tags (list[str]): a list of user generated tags associated with the url

        Returns:
            Page: Instance of an es-Doctype subclass, represents information for page

    """
    orig_text = parse_url(url)
    text = ' '.join(orig_text.split())
    hash_id = mmh3.hash(text) # murmur hash, 32 bit
    page = Page(meta={'id': hash_id}, url=url, body=text, tags='')
    return page


def process_urls(urls):
    pages = list(map(process_url, urls))
    ids = [x._id for x in pages]
    print(ids)
    # [x.save() for x in pages]


class Database(object):
    def __init__(self, **kwargs):
        self.dbargs = kwargs


    def save_url_to_table(self, url):
        with psycopg2.connect(**self.dbargs) as conn:
                with conn.cursor() as cursor:
                    pg_uuid = uuid.uuid4()
                    # check for duplicates
                    cursor.execute('INSERT INTO wp.pages (id, name, created_ts)'
                                    'select \'{}\', \'{}\', current_timestamp '
                                    'WHERE NOT EXISTS '
                                    '(SELECT name FROM wp.pages WHERE name = \'{}\');'.format(
                                        str(pg_uuid), url, url
                                    ))
                conn.commit()
