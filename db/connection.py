from os import getenv

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()
conn = psycopg2.connect(
    user=getenv('USER'),
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
    CREATE TABLE IF NOT EXISTS instagram(
        id BIGSERIAL PRIMARY KEY,
        url TEXT UNIQUE,
        media TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT now()
        )'''
    pin_query = '''
    CREATE TABLE IF NOT EXISTS pinterest(
        id BIGSERIAL PRIMARY KEY,
        url TEXT UNIQUE,
        media TEXT NOT NULL,
        types VARCHAR(15) NOT NULL,
        created_at TIMESTAMP DEFAULT now()
        )'''
    tiktok_query = '''
    CREATE TABLE IF NOT EXISTS tiktok(
        id BIGSERIAL PRIMARY KEY,
        url TEXT UNIQUE,
        media TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT now()
        )'''
    likee_query = '''
    CREATE TABLE IF NOT EXISTS likee(
        id BIGSERIAL PRIMARY KEY,
        url TEXT UNIQUE,
        media TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT now()
        )'''
    cur.execute(query)
    cur.execute(insta_query)
    cur.execute(pin_query)
    cur.execute(tiktok_query)
    cur.execute(likee_query)
    conn.commit()
