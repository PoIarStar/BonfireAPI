from bonfire_session import BonfireSession


class Client:
    def __init__(self, email: str, password: str, token: str = ""):
        """"""
        self.session: BonfireSession = BonfireSession(token)
        self.email: str = email
        self.password: str = password
        self.token: str = token
        #if not self.session.is_auth():
        self.session.login(self.email, self.password)

    def login(self):
        self.session.login(self.email, self.password)

    def is_auth(self):
        self.session.is_auth()
