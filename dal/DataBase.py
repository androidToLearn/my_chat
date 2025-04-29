import psycopg
from dotenv import load_dotenv
import os
load_dotenv()


class DataBase:

    def __init__(self):
        self.cursor = None
        self.conn = None

    def doConnection(self):
        DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
        DATABASE_HOST = os.getenv('DATABASE_HOST')
        DATABASE_DBNAME = os.getenv('DATABASE_DBNAME')
        DATABASE_USER = os.getenv('DATABASE_USER')
        DATABASE_PORT = os.getenv('DATABASE_PORT')
        self.conn = psycopg.connect(dbname=DATABASE_DBNAME, password=DATABASE_PASSWORD,
                                    user=DATABASE_USER, host=DATABASE_HOST, port=DATABASE_PORT)
        self.cursor = self.conn.cursor()
        return self.cursor

    def stopConnection(self):
        self.cursor.close()
        self.conn.close()
