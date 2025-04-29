import psycopg
from dotenv import load_dotenv
import os
load_dotenv()


class DataBase:

    def __init__(self):
        self.cursor = None
        self.conn = None

    def doConnection(self):

        self.conn = psycopg.connect(os.getenv('DATA_BASE_URL'))
        self.cursor = self.conn.cursor()
        return self.cursor

    def stopConnection(self):
        self.cursor.close()
        self.conn.close()
