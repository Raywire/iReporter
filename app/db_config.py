"""Database configuration"""
import psycopg2
import psycopg2.extras
import os

url = os.getenv('DATABASE_URL')
test_url =  os.getenv('DATABASE_URL_TEST')

def connection(url):
    con = psycopg2.connect(url)
    return con

def create_cursor(url):
    conn = connection(url)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return cursor

def create_tables():
    conn = connection(url)
    cursor = conn.cursor()
    queries = tables()

    for query in queries:
        cursor.execute(query)
    conn.commit()

def destroy_tables():
    pass

def tables():
    table1 = """CREATE TABLE IF NOT EXISTS incidents(
        id SERIAL PRIMARY KEY NOT NULL,
        createdOn TIMESTAMP,
        createdBy INT NOT NULL REFERENCES users(id),
        type VARCHAR(20) NOT NULL,
        location VARCHAR(50),
        status VARCHAR(20) NOT NULL,
        Images VARCHAR(500),
        Videos VARCHAR(500),
        title VARCHAR(100),
        comment VARCHAR(1000) NOT NULL
        );"""

    table2 = """CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY NOT NULL,
        firstname VARCHAR(20) NOT NULL,
        lastname VARCHAR(20),
        othernames VARCHAR(20),
        username VARCHAR(20) UNIQUE,
        email VARCHAR(100) UNIQUE,
        phoneNumber VARCHAR(20),
        registered TIMESTAMP,
        isAdmin boolean,
        password VARCHAR(120) NOT NULL,
        public_id VARCHAR(120) NOT NULL
        );"""

    queries = [table2, table1]
    return queries
