import bs4

import mmh3
import requests

from es import Page

urls = [
    'http://www.codethatgrows.com/lessons-learned-from-rust-the-result-monad/',
    'http://blog.pnkfx.org/blog/2015/11/10/gc-and-rust-part-1-specing-the-problem/',
    'http://blog.pnkfx.org/blog/2015/10/27/gc-and-rust-part-0-how-does-gc-work/',
    'http://julienblanchard.com/2015/rust-on-aws-lambda/',
    'https://medium.com/@paulcolomiets/async-io-for-rust-part-ii-33b9a7274e67#.y66omtugh'
]

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


def main():
    # connections.create_connection(hosts=['localhost'], timeout=20)
    # Page.init()
    pages = list(map(process_url, urls))
    ids = [x._id for x in pages]
    [x.save() for x in pages]
    example = Page.get(ids[0])
    import pdb; pdb.set_trace()


if __name__ == '__main__':
    main()