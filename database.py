import hashlib
import psycopg2
import uuid


class Database(object):
    def __init__(self, **kwargs):
        self.dbargs = kwargs

    def save_url_to_table(self, url, hash_as_str):
        with psycopg2.connect(**self.dbargs) as conn:
            page = None
            with conn.cursor() as cursor:
                pg_uuid = uuid.uuid4()
                url_hash = hashlib.md5()
                url_hash.update(url.encode('utf-8'))
                hash_as_str = url_hash.hexdigest()
                page = (str(pg_uuid), url, hash_as_str)
                # check for duplicates
                try:
                    cursor.execute('INSERT INTO wp.pages (id, name, created_ts, md5_hash)'
                                'select \'{}\', \'{}\', current_timestamp, \'{}\' '
                                'WHERE NOT EXISTS '
                                '(SELECT name FROM wp.pages WHERE name = \'{}\');'.format(
                                    str(pg_uuid), url, url, hash_as_str
                                ))
                except psycopg2.IntegrityError as ie:
                    return None

            conn.commit()
            return page
