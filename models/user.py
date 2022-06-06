from datetime import datetime, timedelta

from flask_login import UserMixin
from datetime import date
from dateutil.relativedelta import relativedelta

# TODO: все константы надо выносить в файл конфигурации
DEFAULT_PROBATIONS_NUMBER = 5   # значение доступных тестируемых по умолчанию
DEFAULT_EXPIRATION_MONTHS = 6   # сколько месяцев активна запись пользователя если не указана дата экспирации

class User(UserMixin):
    """
    Класс Пользователь

    Args:
        UserMixin (UserMixin): хз что это, так в документации Flask написано делать
    """    

    user_id = ""
    login = ""
    name = ""
    role = ""
    email = ""
    created_date = ""
    education_module_expiration_date = ""
    probationers_number = DEFAULT_PROBATIONS_NUMBER
    token = ""
    email_confirmed = False

    def __init__(self, _user_id=None, _login="", _name="", _email="", _role="user", _active=True, _created_date="",
                 _education_module_expiration_date="", _probationers_number=DEFAULT_PROBATIONS_NUMBER, _token="",
                 _email_confirmed=False):
        """
        Конструктор класса

        Args:
            _user_id (Int, optional): Id пользователя. Defaults to None
            _login (str, optional): Логин пользователя. Defaults to ""
            _name (str, optional): Имя пользователя. Defaults to ""
            _email (str, optional): Email пользователя. Defaults to ""
            _role (str, optional): Роль пользователя. Defaults to "user"
            _created_date (date, optional): Дата создания пользователя в системе. Defaults to ""
            _education_module_expiration_date (date, optional): Дата до которой пользователь активен. Defaults to "".
            _probationers_number (int, optional): Количество тестируемых, доступное пользователю. Defaults to DEFAULT_PROBATIONS_NUMBER
            _active (bool): Активирован/заблокирован пользователь
        """        

        self.user_id = _user_id
        self.login = _login
        self.name = _name
        self.email = _email
        self.role = _role
        self.probationers_number = _probationers_number
        self.active = _active
        self.token = _token
        self.email_confirmed = _email_confirmed

        # если дата создания не указана, то будем считать что пользователь создан сегодня
        if _created_date == "":
            self.created_date = date.today()
        else:
            self.created_date = _created_date

        if type(self.created_date) is str:
            self.created_date = datetime.datetime.strptime(self.created_date, "%d/%m/%Y")

        if _education_module_expiration_date == "":
            self.education_module_expiration_date = date.today() - timedelta(days=1)
        else:
            if type(_education_module_expiration_date) is str:
                self.education_module_expiration_date = datetime.datetime.strptime(_education_module_expiration_date, "%d/%m/%Y")
            else:
                self.education_module_expiration_date = _education_module_expiration_date

        self.probationers_number = _probationers_number
    
    def is_active(self):
        """
        Возвращает признак того, что учетная запись пользователя активна

        Returns:
            Boolean: True если учетная запись активна и False если нет
        """        

        is_active = False

        if self.active:
            is_active = True
        elif self.education_module_expiration_date >= date.today():
            is_active = True
        
        return is_active
    
    def get_id(self):
        """
        Возвращает id пользователя

        Returns:
            Int: Id пользователя
        """        
        return self.user_id

    def is_admin(self):
        """
        Возвращает признак того, что пользователь обладает правами администратора

        Returns:
            Boolean: True если у пользователя есть права администратора и False если нет
        """        

        if self.role =="superuser":
            return True
        else:
            return False
    
    def is_email_verified(self):
        """
        Возвращает признак того, что пользователь подтвердил свой email адрес

        Returns:
            Boolean: True если у пользователя подтвержденный email адрес и False если нет
        """        

        if self.role =="superuser":
            return True
        else:
            #TODO реализовать логику определения подтвержденного email
            return False
