import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

class Database:

    def __init__(self):

        self.conn = psycopg2.connect(
            os.getenv("DATABASE_URL")
        )

        self.cursor = self.conn.cursor()

    def execute(
        self,
        query,
        params=None
    ):

        self.cursor.execute(
            query,
            params
        )

        self.conn.commit()

    def fetchone(self):

        return self.cursor.fetchone()

    def fetchall(self):

        return self.cursor.fetchall()