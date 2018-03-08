#!/usr/bin/env python
import argparse
import fileinput

from core import process_url
from database import Database


DB_ARGS= {
    'dbname': 'webparse',
    'user': 'webparse_user',
    'password': 'pass325',
    'host': 'localhost'
}
DB = Database(**DB_ARGS)



if __name__ == '__main__':
    parser = argparse.ArgumentParser('Populates the system from a list of urls')
    parser.add_argument('--urls_file', type=str,
                        help='path to lines delimited file of urls',
                        default='urls.txt')
    args = parser.parse_args()
    with open(args.urls_file) as f:
        for line in f.readlines():
            print(line.strip())
            process_url(line.strip(), DB)
