"""Database configuration"""
import psycopg2
import os
from instance.config import APP_CONFIG
from werkzeug import generate_password_hash, check_password_hash

configuration = os.getenv('FLASK_CONFIG')
url = "dbname='doegbut4609qk' host='ec2-54-227-249-201.compute-1.amazonaws.com' port='5432' user='labsbmsbsepgpz' password='71013fe01c407f6385bc2c0e107a6594cf20e8e5c71c05bbbd46d07350133dc7'"


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
    cursor =  conn.cursor()
    cursor.execute(query)
    conn.commit()


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
        public_id VARCHAR(120) NOT NULL UNIQUE
        );"""

    queries = [table2, table1]
    return queries


def create_super_user():
    password = generate_password_hash("1212121")
    test_user = {
        "email": "ryanwire@outlook.com",
        "firstname": "Ryan",
        "isAdmin": True,
        "lastname": "Wire",
        "othernames": "Simiyu",
        "password": password,
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
