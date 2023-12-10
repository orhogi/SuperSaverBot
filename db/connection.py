from os import getenv

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()
conn = psycopg2.connect(
    user="postgres",
    database=getenv('NAME'),
    password=getenv('PASSWORD'),
    host=getenv('HOST'),
    port=5432,
    cursor_factory=DictCursor
)
cur = conn.cursor()


def create_db():
    query = '''
    CREATE TABLE IF NOT EXISTS users(
        id BIGSERIAL PRIMARY KEY,
        telegram_id VARCHAR(60) UNIQUE,
        username VARCHAR(50),
        first_name VARCHAR(128) NOT NULL,
        created_at TIMESTAMP DEFAULT now()
        )'''
    insta_query = '''
    CREATE TABLE IF NOT EXISTS channels(
        id BIGSERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT now()
        )'''
    cur.execute(query)
    cur.execute(insta_query)
    conn.commit()
