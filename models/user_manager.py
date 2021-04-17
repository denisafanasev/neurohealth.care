from models.user import User


class UserManager():

    def get_user(self, _user_id):
        user = None
        if _user_id is not None:
            user = User(_user_id, "Admin", "Admin")

        return user

    def get_user_id(self, _login, _password):
        if _login == "admin" and _password == "admin":
            return 123
        
        return None
