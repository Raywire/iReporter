"""Database configuration"""
import psycopg2
import os

url = "dbname='ireporter' host='localhost' port='5432' user='raywire' password='raywire2018'"

db_url = os.getenv('DATABASE_URL')

class DataBaseConfig:
    """Database configuration class"""
    def connection(url):
        con = psycopg2.connect(url)
        return con


    def init_db():
        con = connection(url)
        return con


    def create_tables():
        conn = connection(url)
        cur = conn.cursor()
        queries = tables()

        for query in queries:
            cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()


    def destroy_tables():
        pass


    def tables():
        table1 = """CREATE TABLE IF NOT EXISTS incidents (
            id SERIAL PRIMARY KEY NOT NULL,
            createdOn TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
            createdBy NUMERIC NOT NULL,
            type VARCHAR(20) NOT NULL,
            location VARCHAR(50),
            status VARCHAR(20) NOT NULL,
            Images VARCHAR(1000),
            Videos VARCHAR(1000),
            comment VARCHAR(1000) NOT NULL
            );"""

        table2 = """CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY NOT NULL,
            firstname VARCHAR(20) NOT NULL,
            lastname VARCHAR(20),
            othernames VARCHAR(20),
            username VARCHAR(20) NOT NULL,
            email VARCHAR(100),
            phoneNumber VARCHAR(20),
            registered TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
            isAdmin boolean,
            password VARCHAR(120) NOT NULL
            );"""

        queries = [table1, table2]
        return queries
