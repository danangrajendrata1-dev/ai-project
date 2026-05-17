from models.user import User

user = User()

class AuthService:

    def login(
        self,
        username,
        password
    ):

        return user.login(
            username,
            password
        )

    def register(
        self,
        username,
        password
    ):

        return user.register(
            username,
            password
        )