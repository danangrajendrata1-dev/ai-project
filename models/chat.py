from core.database import Database


class Chat:

    def __init__(self):

        self.db = Database()

    def save(self, session_id, role, message):

        query = """
        INSERT INTO chats (
            session_id,
            role,
            message
        )
        VALUES (%s, %s, %s)
        """

        self.db.execute(
            query,
            (session_id, role, message)
        )

    def load(self, session_id):

        query = """
        SELECT role, message
        FROM chats
        WHERE session_id = %s
        ORDER BY id ASC
        """

        self.db.execute(query, (session_id,))

        rows = self.db.fetchall()

        return [
            {
                "role": r[0],
                "content": r[1]
            }
            for r in rows
        ]

    def clear(self, session_id):

        query = """
        DELETE FROM chats
        WHERE session_id = %s
        """

        self.db.execute(query, (session_id,))