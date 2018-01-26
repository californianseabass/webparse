DROP ROLE IF EXISTS webparse_admin;
CREATE ROLE webparse_admin;
ALTER ROLE webparse_admin WITH LOGIN;
ALTER ROLE webparse_admin WITH PASSWORD 'pass4';

CREATE SCHEMA IF NOT EXISTS public AUTHORIZATION webparse_admin;

CREATE SCHEMA IF NOT EXISTS wp AUTHORIZATION webparse_admin;
GRANT ALL PRIVILEGES ON SCHEMA wp TO webparse_admin;
GRANT ALL PRIVILEGES ON DATABASE webparse to webparse_admin;

CREATE ROLE webparse_user;
ALTER ROLE webparse_user with LOGIN;
ALTER ROLE webparse_user WITH PASSWORD 'pass325';
GRANT ALL PRIVILEGES ON SCHEMA wp to webparse_user;

CREATE TABLE wp.users
(
  id uuid PRIMARY KEY,
  password VARCHAR NOT NULL,
  email VARCHAR UNIQUE NOT NULL,
  username VARCHAR NOT NULL
) TABLESPACE pg_default;

CREATE TABLE wp.pages
(
  id uuid PRIMARY KEY,
  name varchar UNIQUE NOT NULL,
  created_ts timestamp NOT NULL,
  md5_hash varchar UNIQUE NOT NULL
) TABLESPACE pg_default;


GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA wp TO webparse_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA wp to webparse_user;
