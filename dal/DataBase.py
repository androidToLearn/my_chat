import psycopg
import os
from dotenv import load_dotenv
load_dotenv()


class DataBase:

    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DATABASE_HOST = os.getenv('DATABASE_HOST')
    DATABASE_DBNAME = os.getenv('DATABASE_DBNAME')
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PORT = os.getenv('DATABASE_PORT')

    def __init__(self):
        self.cursor = None
        self.conn = None

    def doConnection(self):
        self.conn = psycopg.connect(dbname=DataBase.DATABASE_DBNAME, password=DataBase.DATABASE_PASSWORD,
                                    user=DataBase.DATABASE_USER, host=DataBase.DATABASE_HOST, port=DataBase.DATABASE_PORT)
        self.cursor = self.conn.cursor()
        return self.cursor

    def stopConnection(self):
        self.cursor.close()
        self.conn.close()
