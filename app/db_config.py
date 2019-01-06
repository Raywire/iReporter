"""Database configuration"""
import psycopg2
import os
from instance.config import APP_CONFIG
from werkzeug import generate_password_hash, check_password_hash
import datetime
import uuid

configuration = os.getenv('FLASK_CONFIG')
url = APP_CONFIG[configuration].DATABASE_URL

password = generate_password_hash(os.getenv('SUPER_USER_PASSWORD'))
email = os.getenv('SUPER_USER_EMAIL')
username = os.getenv('SUPER_USER_USERNAME')
firstname = os.getenv('SUPER_USER_FIRSTNAME')
lastname = os.getenv('SUPER_USER_LASTNAME')
othernames = os.getenv('SUPER_USER_OTHERNAMES')
phonenumber = os.getenv('SUPER_USER_PHONENUMBER')
public_id = str(uuid.uuid4())
registered = datetime.datetime.utcnow()


def connection(url):
    con = psycopg2.connect(url)
    return con


def init_database():
    con = connection(url)
    return con


def create_tables():
    conn = connection(url)
    cursor = conn.cursor()
    queries = tables()

    for query in queries:
        cursor.execute(query)
    conn.commit()


def destroy_tables():
    query = """DROP TABLE IF EXISTS users, incidents;"""
    test_url = os.getenv('DATABASE_URL_TEST')
    conn = connection(test_url)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def tables():
    table1 = """CREATE TABLE IF NOT EXISTS incidents(
        id SERIAL PRIMARY KEY NOT NULL,
        createdOn TIMESTAMP,
        createdBy INT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
        type VARCHAR(20) NOT NULL,
        location VARCHAR(50),
        status VARCHAR(20) NOT NULL,
        Images VARCHAR(500) NULL,
        Videos VARCHAR(500) NULL,
        title VARCHAR(100),
        comment VARCHAR(2000) NOT NULL
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
        public_id VARCHAR(120) NOT NULL UNIQUE
        );"""

    queries = [table2, table1]
    return queries

if configuration == 'testing':
    public_id = "f3b8a1c3-f775-49e1-991c-5bfb963eb419"

user = {
    "email": email,
    "firstname": firstname,
    "isAdmin": True,
    "lastname": lastname,
    "othernames": othernames,
    "password": password,
    "phoneNumber": phonenumber,
    "public_id": public_id,
    "registered": registered,
    "username": username
}    

query = """INSERT INTO users (firstname,lastname,othernames,email,phoneNumber,username,registered,password,isAdmin,public_id) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',{8},'{9}');""".format(
    user['firstname'], user['lastname'], user['othernames'], user['email'], user['phoneNumber'], user['username'], user['registered'], user['password'], user['isAdmin'], user['public_id'])

def create_super_user():

    conn = connection(url)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
    except:
        return "already exists"
