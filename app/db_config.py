"""Database configuration"""
import psycopg2
import psycopg2.extras
import os

url = os.getenv('DATABASE_URL')
test_url = os.getenv('DATABASE_URL_TEST')


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


def create_test_user():
    test_user = {
        "email": "ryanwire@outlook.com",
        "firstname": "Ryan1",
        "isAdmin": True,
        "lastname": "Wire",
        "othernames": "Simiyu",
        "password": "pbkdf2:sha256:50000$ziQztAJR$ea5d5a2cc01a0d919d60fe803ced2a8c8f0974f018607012f87802dc116f1ead",
        "phoneNumber": "0727272727",
        "public_id": "f3b8a1c3-f775-49e1-991c-5bfb963eb419",
        "registered": "Sat, 08 Dec 2018 08:34:45 GMT",
        "username": "ray"
    }
    query = """INSERT INTO users (firstname,lastname,othernames,email,phoneNumber,username,registered,password,isAdmin,public_id) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',{8},'{9}');""".format(
        test_user['firstname'], test_user['lastname'], test_user['othernames'], test_user['email'], test_user['phoneNumber'], test_user['username'], test_user['registered'], test_user['password'], test_user['isAdmin'], test_user['public_id'])
    conn = connection(url)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
    except:
        return "already exists"
