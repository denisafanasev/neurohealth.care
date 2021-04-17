from models.user_manager import UserManager


class LoginService():
    
    def get_user(self, _user_id):

        user_manager = UserManager()

        user = user_manager.get_user(_user_id)

        return user
    
    def get_user_id(self, _login, _password):

        user_manager = UserManager()

        user_id = user_manager.get_user_id(_login, _password)

        return user_id
