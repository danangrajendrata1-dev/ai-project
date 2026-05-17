import os
import psycopg2

class Database:

    def __init__(self):

        self.conn = psycopg2.connect(
            os.getenv("DATABASE_URL")
        )

    def execute(self, query, params=None):

        cursor = self.conn.cursor()

        cursor.execute(query, params)

        self.conn.commit()

        cursor.close()

    def fetchone(self, query, params=None):

        cursor = self.conn.cursor()

        cursor.execute(query, params)

        result = cursor.fetchone()

        cursor.close()

        return result

    def fetchall(self, query, params=None):

        cursor = self.conn.cursor()

        cursor.execute(query, params)

        result = cursor.fetchall()

        cursor.close()

        return result