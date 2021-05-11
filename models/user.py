from flask_login import UserMixin


class User(UserMixin):
    """
    Класс Пользователь

    Args:
        UserMixin (UserMixin): хз что это, так в документации Flask написано делать
    """    

    id = ""
    login = ""
    name = ""
    role = ""
    email = ""

    def __init__(self, _id=None, _login="", _name="", _email="", _role="user"):
        """
        Конструктор класса

        Args:
            _id (Int, optional): Id пользователя. Defaults to None.
            _login (str, optional): Логин пользователя. Defaults to "".
            _name (str, optional): Имя пользователя. Defaults to "".
            _email (str, optional): Email пользователя. Defaults to "".
            _role (str, optional): Роль пользователя. Defaults to "user".
        """        

        self.id = _id
        self.login = _login
        self.name = _name
        self.email = _email
        self.role = _role
