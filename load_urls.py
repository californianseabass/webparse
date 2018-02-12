"""/usr/bin/env python

Usage:
    load_urls.py urls.txt

"""
from database import Database
import sys

from core import process_url



def main(input_file):
    dbargs = {'dbname': 'webparse', 'user': 'webparse_user', 'password': 'pass325', 'host': 'localhost'}
    db = Database(**dbargs)
    with open(input_file) as f:
        for line in f.readlines():
            process_url(line.strip(), db)


if __name__ == '__main__':
    main(sys.argv[1])
