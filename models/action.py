class Action():
    """
    Класс действий
    """

    def __init__(self, _user_login="", _action=""):
        """
        Конструктор класса

        Args:
            _user_login: логин пользователя
            _action: действие, которое совершил пользователь
        """

        self.user_login = _user_login
        self.action = _action