import hashlib
import psycopg2
import uuid


DB_ARGS = {'dbname': 'webparse', 'user': 'webparse_user', 'password': 'pass325', 'host': 'localhost'}

class Database(object):
    def __init__(self, **kwargs):
        self.dbargs = kwargs

    def save_url_to_table(self, url):
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
                    cursor.execute(
                        'INSERT INTO wp.pages (id, name, created_ts, md5_hash) '
                        'select \'{}\', \'{}\', current_timestamp, \'{}\' '
                        'WHERE NOT EXISTS '
                        '(SELECT name FROM wp.pages WHERE md5_hash = \'{}\');'.format(
                            str(pg_uuid), url, hash_as_str, hash_as_str))
                    conn.commit()
                except psycopg2.IntegrityError as ie:
                    return None

            conn.commit()
            return page

    def get_urls(self):
        with psycopg2.connect(**self.dbargs) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT name, title FROM wp.pages ORDER BY created_ts desc;')
                rows = list(cursor.fetchall())
                for row in rows:
                    print(rows)
                return rows


    def get_url_by_md5_hash(self, md5_hash):
        with psycopg2.connect(**self.dbargs) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT name FROM wp.pages where md5_hash = \'{md5_hash}\';')
                return cursor.fetchone()
