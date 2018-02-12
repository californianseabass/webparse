#!/usr/bin/env python3

from core import search_pages

def main():
    while True:
        print('Search term: ')
        search_string = input()
        print(search_string)
        search_pages(search_string.strip())
    # get user input
    # subtmit query to search api, in this case our


if __name__ == '__main__':
    main()
