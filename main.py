import bs4
from elasticsearch_dsl import DocType, String, Date,
import mmh3
import requests


urls = [
    'http://www.codethatgrows.com/lessons-learned-from-rust-the-result-monad/',
    'http://blog.pnkfx.org/blog/2015/11/10/gc-and-rust-part-1-specing-the-problem/',
    'http://blog.pnkfx.org/blog/2015/10/27/gc-and-rust-part-0-how-does-gc-work/',
    'http://julienblanchard.com/2015/rust-on-aws-lambda/',
    'https://medium.com/@paulcolomiets/async-io-for-rust-part-ii-33b9a7274e67#.y66omtugh'
]

# document, hashtags, url, store date
class Page(DocType):
    url = String(analyzer='snowball')
    hashtags =

def process_url(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    return text

def save_to_es(url, text):
    pass

def create_index():
    # document, hashtags, url, store date
    pass

def main():
    for url in urls[0:1]:
        orig_text = process_url(url)
        text = ' '.join(orig_text.split())
        hash_id = mmh3.hash64(text)
        print(hash_id)

if __name__ == '__main__':
    main()
