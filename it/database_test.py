import psycopg2

from database import Database, DB_ARGS


TEST_URL= 'https://gravitational.com/blog/running-postgresql-on-kubernetes/'


def test_saving_to_postgres():
    db = Database(**DB_ARGS)
    db.save_url_to_table(TEST_URL)
    with psycopg2.connect(**DB_ARGS) as conn:
            with conn.cursor() as cursor:
                # check for duplicates
                cursor.execute('SELECT id, name FROM wp.pages where name = \'{}\';'.format(
                                   TEST_URL
                                ))
                result = cursor.fetchone()
                assert result[1] == TEST_URL
            conn.commit()
