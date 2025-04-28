import psycopg


class DataBase:

    DATABASE_PASSWORD = "newpassword"
    DATABASE_HOST = 'localhost'
    DATABASE_DBNAME = 'postgres'
    DATABASE_USER = 'postgres'
    DATABASE_PORT = '5432'

    def __init__(self):
        self.cursor = None
        self.conn = None

    def doConnection(self):
        self.conn = psycopg.connect(dbname='postgres', password='newpassword',
                                    user='postgres', host='localhost', port='5432')
        self.cursor = self.conn.cursor()
        return self.cursor

    def stopConnection(self):
        self.cursor.close()
        self.conn.close()
