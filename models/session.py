from core.database import Database


class Session:

    def __init__(self):

        self.db = Database()

    # CREATE SESSION
    def create(self, user_id, title="New Chat"):

        query = """
        INSERT INTO chat_sessions (
            user_id,
            title
        )
        VALUES (%s, %s)
        RETURNING id
        """

        self.db.execute(query, (user_id, title))

        return self.db.fetchone()[0]

    # GET ALL SESSION USER
    def get_all(self, user_id):

        query = """
        SELECT id, title
        FROM chat_sessions
        WHERE user_id = %s
        ORDER BY created_at DESC
        """

        self.db.execute(query, (user_id,))

        return self.db.fetchall()

    # GET SINGLE SESSION (optional tapi bagus)
    def get_by_id(self, session_id, user_id):

        query = """
        SELECT id, title
        FROM chat_sessions
        WHERE id = %s AND user_id = %s
        """

        self.db.execute(query, (session_id, user_id))

        return self.db.fetchone()

    # UPDATE TITLE
    def update_title(self, session_id, user_id, title):

        query = """
        UPDATE chat_sessions
        SET title = %s
        WHERE id = %s AND user_id = %s
        """

        self.db.execute(
            query,
            (title, session_id, user_id)
        )

    # DELETE SESSION
    def delete(self, session_id, user_id):

        # 1. delete chats dulu (biar tidak orphan data)
        self.db.execute(
            """
            DELETE FROM chats
            WHERE session_id = %s
            """,
            (session_id,)
        )

        # 2. delete session
        self.db.execute(
            """
            DELETE FROM chat_sessions
            WHERE id = %s AND user_id = %s
            """,
            (session_id, user_id)
        )