#!/usr/bin/env python
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
    for line in fileinput.input():
        print(line.strip())
        process_url(line.strip(), DB)
