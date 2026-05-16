import bcrypt
from core.database import Database
from core.security import create_access_token


class User:

    def __init__(self):
        self.db = Database()

    # =====================
    # REGISTER
    # =====================
    def register(self, username, password):

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        query = """
        INSERT INTO users (username, password)
        VALUES (%s, %s)
        """

        self.db.execute(query, (username, hashed))


    # =====================
    # VERIFY PASSWORD
    # =====================
    def verify_password(self, plain_password, hashed_password):

        return bcrypt.checkpw(
            plain_password.encode(),
            hashed_password.encode()
        )


    # =====================
    # LOGIN (JWT)
    # =====================
    def login(self, username, password):

        user = self.db_get_user(username)

        if user and self.verify_password(password, user["password"]):

            token = create_access_token({
                "user_id": user["id"],
                "username": user["username"]
            })

            return {
                "access_token": token,
                "user_id": user["id"]
            }

        return None


    # =====================
    # GET USER
    # =====================
    def db_get_user(self, username):

        query = """
        SELECT id, username, password
        FROM users
        WHERE username = %s
        """

        result = self.db.fetch_one(query, (username,))

        return result