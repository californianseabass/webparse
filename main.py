import avro.schema as avro_schema
from avro.datafile import DataFileReader, DataFileWriter

from core import process_urls
from wp_avro import start_server

CONST_URLS = [
    'http://www.codethatgrows.com/lessons-learned-from-rust-the-result-monad/',
    'http://blog.pnkfx.org/blog/2015/11/10/gc-and-rust-part-1-specing-the-problem/',
    'http://blog.pnkfx.org/blog/2015/10/27/gc-and-rust-part-0-how-does-gc-work/',
    'http://julienblanchard.com/2015/rust-on-aws-lambda/',
    'https://medium.com/@paulcolomiets/async-io-for-rust-part-ii-33b9a7274e67#.y66omtugh'
]





def main():
    start_server()

if __name__ == '__main__':
    main()
