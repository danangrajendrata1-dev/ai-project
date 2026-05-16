import os
import psycopg2

class Database:

    def __init__(self):

        self.conn = psycopg2.connect(
            os.getenv("postgresql://neondb_owner:npg_ly9AnVpOX8bE@ep-noisy-dream-aouwl360.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
        )

    def execute(self, query, params=None):

        cur = self.conn.cursor()
        cur.execute(query, params)
        self.conn.commit()
        cur.close()

    def fetch_one(self, query, params=None):

        cur = self.conn.cursor()
        cur.execute(query, params)
        result = cur.fetchone()
        cur.close()

        return result