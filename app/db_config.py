"""Database configuration"""
import psycopg2
import os
from werkzeug import generate_password_hash
import datetime

password = generate_password_hash(os.getenv('SUPER_USER_PASSWORD'))
email = os.getenv('SUPER_USER_EMAIL')
username = os.getenv('SUPER_USER_USERNAME')
firstname = os.getenv('SUPER_USER_FIRSTNAME')
lastname = os.getenv('SUPER_USER_LASTNAME')
othernames = os.getenv('SUPER_USER_OTHERNAMES')
phonenumber = os.getenv('SUPER_USER_PHONENUMBER')
registered = datetime.datetime.utcnow()

admin = {
  "type": "service_account",
  "project_id": "ireporter-1545750372947",
  "private_key_id": "2ba6f9a5eff6454376b88e2d29560f9e76e350b8",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCW1ZRM9vx/e7o2\nkFlTuQOJn4iqMkT12a2FPjzVnkm7LPoxjnA2VQbCLPoK0DAPxSENvew30MkBOyZl\nFDyfc08GHz4ErRh+1Cc6+i95/0GilE9g48vXAHvdtoJKXVVfh2BWjn+swiEj+R/o\nin5ySLxXxj5dI9M7ZZrEyK7KoVRv8Q+fMtN7oMDuJRXxSgN1fwYvgvBmsXO5AeoW\n5hqJgdIniNKS1iji6HcgL/1CIQZ4rfjqFdxEFp5OvfkAL6MSREDmQjzAYcdCGtBy\n8//AFaTnC4UAdXFT1uuhcbECdwi5oiPmBrqXBepW5H6F4bmg/wxrPthlINwARlm/\n9jRzja7bAgMBAAECggEABMb08HnDcNeJWUsPGTYQj55MOh+8zBCTN1d2SR8Un2dY\nRpOH/aCJxe1Iv2jtQhfwk7qCgxi2FQzmNWiuVtp/E+bkvvSAhHEnC5jQQiE8gfAH\n55NaFGWBMXojUZmifOkREGITrHQQOqRxnJrY+w5PW3RS61OZesByu215DmqM/b1B\n/tcbmps9Qn7fFV3jN5K9YFG/m7bxyW73ro27AEPa2eJfOl8JJANcxfc35CNyOwsE\nu3xnznMC5IGIp8bzgABkwe8pzI/+CLnJmIw34FfsMzuVAO0ieTUEC20pa6cibhGT\n5bTiJ+2AJbb6Q8q/45aaPSkRX/OpdxWY6pkpKth5uQKBgQDRVBXBtE/7O5diiiq5\nWK56Ru9/z1WQ5BXlviiMKuDF5dmjz9tKqA94SK5KYOTGLEpWKMSadNiubsmVa2gS\nFpFAkvcd1V8MgcwAffMrT1d/cRMhFqdQV5oLV7LcenzcZGB2HBlT6pBzQgJvWPZD\niT635t4nNcm46MaOG1YDO0kEvwKBgQC4ds1XSrn+GAAAQGYibKh4IG5IvQfqg5fO\njMcREB/SHcRCR7IexMFM9DQOoygksYiKUF4hRG59Bz7c3LtSdXFgUibvQ0LfK2I3\n4trfeJ6rlnmdcpC90ubXG1iwAY6dptyMnjZEaP8YtGEjBP+6NrBG5buF7vSfxcMi\nu9gXZq+Q5QKBgQCATuUjHY4k9cr+OKilgYk5JD/rfL/7FwOhFiUufZ3XT+NOuLq3\nETqiRRKoPqocGsvZ8hVIg7TJftkLQJHC/Jg+F5dnbwFa3jiYWJt0AaclU78g+gzG\nf1vJ9hCJen8MbG6AFwsjV9UBAQYTEFmq3fZWrSmgqSSjtfL26iSXyIAiawKBgHc+\n5ZNujTnDTgzblKrgTzAI1wJSoNFrbDFsNCvFnqx37a1jJ7RYQRV8MELeGk9OLRQs\nzAz5beuJSYwBbV7q6PX5ZY36jzoxk3bJQfCAyyHlTo0HyKXNtsiLtxNgjk8/1Qda\nJ36l2XKg+MJosuAwBlhunoEAbkby0yibAiBuk0Q5AoGAYsOZO1MNsOYREHOVT96g\nFexddSxRuTidc+ScRYiLou0jb3aVneIMP4ar6jAFf4l+XHEPPKkhpvCzZNlGIXq8\n47F8gz9JtHae7vWvqgKHQq6hOBRpjVxLMgyWQQ9MNQhZ8/cHhNvbv5/7Kd9R0BHM\nJNoPP9Rw+6aF+PTtVKDyWjM=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-lkgwy@ireporter-1545750372947.iam.gserviceaccount.com",
  "client_id": "111716786571886039692",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-lkgwy%40ireporter-1545750372947.iam.gserviceaccount.com"
}

config = {
    "apiKey": "AIzaSyBI4J505aUT7vZDQE05vW0Mzy_gL8Ci4dM",
    "authDomain": "ireporter-1545750372947.firebaseapp.com",
    "databaseURL": "https://ireporter-1545750372947.firebaseio.com",
    "projectId": "ireporter-1545750372947",
    "storageBucket": "ireporter-1545750372947.appspot.com",
    "messagingSenderId": "938809178063",
    "serviceAccount": admin
}

def connection(url):
    con = psycopg2.connect(url)
    return con


def init_database(url):
    con = connection(url)
    return con


def create_tables(url):
    conn = connection(url)
    cursor = conn.cursor()
    queries = tables()

    for query in queries:
        cursor.execute(query)
    conn.commit()


def destroy_tables(url):
    query = """DROP TABLE IF EXISTS users, incidents;"""
    test_url = os.getenv('DATABASE_URL_TEST')
    conn = connection(url)
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
        comment VARCHAR(5000) NOT NULL
        );"""

    table2 = """CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY NOT NULL,
        firstname VARCHAR(20) NOT NULL,
        lastname VARCHAR(20),
        othernames VARCHAR(20),
        username VARCHAR(20) UNIQUE,
        email VARCHAR(100) UNIQUE,
        emailVerified boolean DEFAULT FALSE,
        phoneNumber VARCHAR(20),
        registered TIMESTAMP,
        isAdmin boolean,
        isActive boolean DEFAULT TRUE,
        password VARCHAR(120) NOT NULL,
        public_id VARCHAR(120) NOT NULL UNIQUE,
        photourl VARCHAR(150) DEFAULT NULL
        );"""

    queries = [table2, table1]
    return queries

def create_super_user(url, public_id):  

    user = {
        "email": email,
        "firstname": firstname,
        "isAdmin": True,
        "isActive": True,
        "lastname": lastname,
        "othernames": othernames,
        "password": password,
        "phoneNumber": phonenumber,
        "public_id": public_id,
        "registered": registered,
        "username": username
    }

    query = """INSERT INTO users (firstname,lastname,othernames,email,phoneNumber,username,registered,password,isAdmin,public_id,isActive) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}',{8},'{9}','{10}');""".format(
        user['firstname'], user['lastname'], user['othernames'], user['email'], user['phoneNumber'], user['username'], user['registered'], user['password'], user['isAdmin'], user['public_id'], user['isActive'])
    
    conn = connection(url)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
    except:
        return "already exists"
