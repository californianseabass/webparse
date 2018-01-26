import psycopg2

from core import generate_url_hash
from database import Database


TEST_URL= 'https://gravitational.com/blog/running-postgresql-on-kubernetes/'


def test_saving_to_postgres():
    dbargs = {'dbname': 'webparse', 'user': 'webparse_user', 'password': 'pass325', 'host': 'localhost'}
    db = Database(**dbargs)
    db.save_url_to_table(TEST_URL, generate_url_hash(TEST_URL))
    with psycopg2.connect(**dbargs) as conn:
            with conn.cursor() as cursor:
                # check for duplicates
                cursor.execute('SELECT id, name FROM wp.pages where name = \'{}\';'.format(
                                   TEST_URL
                                ))
                result = cursor.fetchone()
                assert result[1] == TEST_URL
            conn.commit()
