from datetime import date
import datetime


class Action():
    """
    Класс действий
    """

    def __init__(self, _id=None, _user_login="", _action="", _created_date=None, _comment_action=''):
        """
        Конструктор класса

        Args:
            _user_login: логин пользователя
            _action: действие, которое совершил пользователь
            _create_time: дата, когда была записана действие
        """

        self.id = _id
        self.user_login = _user_login
        self.action = _action
        self.comment_action = _comment_action

        if _created_date is None:
            self.created_date = date.today()
        else:
            self.created_date = _created_date

        if type(self.created_date) is str:
            self.created_date = datetime.datetime.strptime(self.created_date, "%d/%m/%Y %H:%M:%S")