from flask_login import UserMixin


class User(UserMixin):

    id = ""
    login = ""
    name = ""

    def __init__(self, _user_id, _login, _name):
        self.user_id = _user_id
        self.login = _login
        self.name = _name
