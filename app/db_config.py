"""Database configuration"""
import psycopg2

url = "dbname='ireporter' host='localhost' port='5432' user='raywire' password='raywire2018'"
test_url = "dbname='test_ireporter' host='localhost' port='5432' user='raywire' password='raywire2018'"

def connection(url):
    con = psycopg2.connect(url)
    return con

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
        createdBy INT NOT NULL,
        type VARCHAR(20) NOT NULL,
        location VARCHAR(50),
        status VARCHAR(20) NOT NULL,
        Images VARCHAR(500),
        Videos VARCHAR(500),
        comment VARCHAR(1000) NOT NULL
        );"""

    table2 = """CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY NOT NULL,
        firstname VARCHAR(20) NOT NULL,
        lastname VARCHAR(20),
        othernames VARCHAR(20),
        username VARCHAR(20) NOT NULL,
        email VARCHAR(100),
        phoneNumber VARCHAR(20),
        registered TIMESTAMP,
        isAdmin boolean,
        password VARCHAR(120) NOT NULL
        );"""

    queries = [table1, table2]
    return queries
