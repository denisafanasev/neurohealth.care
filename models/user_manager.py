import hashlib

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from itsdangerous import URLSafeTimedSerializer

from models.user import User
from data_adapters.data_store import DataStore

from error import UserManagerException
import config


class UserManager():
    """
    Класс модели управления пользователями, ведения списка пользователей
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """

    def hash_password(self, _password):
        """
        Генерирует hash функцию от пароля

        Args:
            _password (String): пароль

        Returns:
            String: представление результата hash функции
        """

        return hashlib.md5(_password.encode()).hexdigest()

    def create_token(self, email):
        """создание токена по email адресу

        Args:
            email (string): email адрес

        Returns:
            string: токен
        """

        serializer = URLSafeTimedSerializer(config.SECRET_KEY)
        return serializer.dumps(email, salt=config.SECURITY_PASSWORD_SALT)

    def validate_password(self, _password):
        """
        Проверка пароля на корректное значение

        Args:
            _password (String): пароль

        Raises:
            UserManagerException: ошибка корректности значения пароля
        """

        if (len(_password) < 5) or (len(_password) > 20):
            raise UserManagerException("неверная длинная пароля, укажите минимум 5 и максимум 20 символов")

    def validate_role(self, _role):
        """
        Проверка корректности указания роли пользователя в системе

        Args:
            _role (String): роль пользователя user/superuser

        Raises:
            UserManagerException: ошибка корректности указанного значения роли
        """

        if _role != "superuser" and _role != "user":
            raise UserManagerException("Роль пользователя задана не верно")

    def validate_login(self, _login):
        """
        Проверка корректности значения логина пользователя

        Args:
            _login (String): логин пользователя

        Raises:
            UserManagerException: ошибка корректности указанного логина пользователя
        """

        if (len(_login) < 3) or (len(_login) > 10):
            raise UserManagerException("неверная длинная логина пользователя, укажите минимум 3 символа и максимум 10")

    def user_row_to_user(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о пользователи в структуру User

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            User: пользователь
        """

        # создадим пользователя с указанием обязательных атрибутов
        # note that doc_id from the table used as a user_id
        try:
            user = User(_data_row.doc_id, _data_row['login'], _data_row['name'], _data_row['email'], _data_row['role'],
                        _data_row['active'])
        except KeyError as error:
            raise UserManagerException("DB structure error: no attribute " + error.args[0])

        # проверим наличие в структуре хранения необязательных атрибутов

        if _data_row.get('probationers_number') is not None:
            user.probationers_number = int(_data_row['probationers_number'])
        else:
            user.probationers_number = 5

        if _data_row.get('created_date') is not None:
            user.created_date = datetime.strptime(_data_row['created_date'], '%d/%m/%Y')
        else:
            user.created_date = datetime.strptime("01/01/1990", '%d/%m/%Y')

        if _data_row.get('education_module_expiration_date') is not None:
            user.education_module_expiration_date = datetime.strptime(_data_row['education_module_expiration_date'],
                                                                      '%d/%m/%Y')
        else:
            user.education_module_expiration_date = datetime.today()

        if _data_row.get('token') is not None:
            user.token = _data_row['token']
        else:
            user.token = ""

        if _data_row.get('email_confirmed') is not None:
            user.email_confirmed = _data_row['email_confirmed']
        else:
            user.email_confirmed = False

        date_today = datetime.today()

        if user.role == 'superuser':
            user.education_module_expiration_date += relativedelta(year=datetime.today().year + 10)

        if date_today.date() > user.education_module_expiration_date.date():
            user.active_education_module = "inactive"
        else:
            if user.education_module_expiration_date - date_today < timedelta(days=31):
                user.active_education_module = "ends"
            else:
                user.active_education_module = "active"

        return user

    def get_user_by_id(self, _user_id):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)
        """

        user = None

        data_store = DataStore("users")
        user_data = data_store.get_row_by_id(_user_id)

        if user_data is not None:

            user = self.user_row_to_user(user_data)
            
            if user_data.get("education_module_expiration_date") is None:

                self.chenge_user(_login=user.login, _name=user.name, _email=user.email, _role=user.role,
                                 _probationers_number=user.probationers_number, _created_date=user.created_date,
                                 _education_module_expiration_date=user.education_module_expiration_date,
                                 _token=user.token, _email_confirmed=user.email_confirmed)

            elif user_data.get("token") is None:

                self.chenge_user(_login=user.login, _name=user.name, _email=user.email, _role=user.role,
                                 _probationers_number=user.probationers_number, _created_date=user.created_date,
                                 _education_module_expiration_date=user.education_module_expiration_date,
                                 _token=user.token, _email_confirmed=user.email_confirmed)

            elif user_data.get("email_confirmed") is None:

                self.chenge_user(_login=user.login, _name=user.name, _email=user.email, _role=user.role,
                                 _probationers_number=user.probationers_number, _created_date=user.created_date,
                                 _education_module_expiration_date=user.education_module_expiration_date,
                                 _token=user.token, _email_confirmed=user.email_confirmed)

        return user

    def get_user(self, _login, _password):
        """
        Возвращает пользователя по логину и паролю

        Args:
            _login   - Required  : current iteration (String)
            _password   - Required  : current iteration (String)
        """

        user = None

        login = _login.lower().strip()
        password = self.hash_password(_password)

        data_store = DataStore("users")

        user_data = data_store.get_rows({"login": login, "password": password})

        # проверим, что у нас данному набору логин и пароль соответсвует только одна запись пользователя
        if len(user_data) > 1:
            raise UserManagerException("Ошибка в базе данных пользователей")

        if len(user_data) == 0:
            raise UserManagerException("Указаны неверные данные для входа")

        # получаем объект Пользователь
        user = self.user_row_to_user(user_data[0])

        return user

    def get_user_by_login(self, _login):
        """
        Возвращает пользователя по логину

        Args:
            _login   - Required  : login пользователя (String)
        """

        user = None

        login = _login.lower().strip()
        data_store = DataStore("users")

        user_data = data_store.get_rows({"login": login})

        if len(user_data) > 1:
            raise UserManagerException("Ошибка в базе данных пользователей, login не уникальный")

        if len(user_data) == 1:
            user = self.user_row_to_user(user_data[0])

        return user

    def get_user_by_email(self, _email):
        """
        Возвращает пользователя по email

        Args:
            _email   - Required  : email пользователя (String)
        """

        user = None

        email = _email.lower().strip()
        data_store = DataStore("users")

        user_data = data_store.get_rows({"email": email})

        if len(user_data) > 1:
            raise UserManagerException("Ошибка в базе данных пользователей, email не уникальный")

        if len(user_data) == 1:
            user = self.user_row_to_user(user_data[0])

        return user

    def get_users(self, _user_id):
        """
        Возвращает список пользователей в системе, в соответствии с ролью пользователя, который запрашивает список

        Args:
            None

        Returns:
            List: список пользователей с типом User
        """

        users = []

        data_store = DataStore("users")

        users_list_data = data_store.get_rows()

        for user_data in users_list_data:

            user = self.user_row_to_user(user_data)

            if self.get_user_role(_user_id) == "superuser":
                users.append(user)
            else:
                if self.get_user_by_id(_user_id) == user.user_id:
                    users.append(user)

        return users

    def is_there_users(self):
        """
        Проверяем, есть ли в системе пользователи вообще

        Args:
            None
        """

        data_store = DataStore("users")

        data = data_store.get_rows_count()

        if data != 0:
            return True

        return False

    def create_user(self, _login, _name, _password, _password2, _email, _role, _probationers_number):
        """
        Процедура создания нового пользователя в системе

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _email (String): email пользователя
            _role (String): роль пользователя [user/superuser]
            _probationers_number (Integer): количество доступных тестирумых

        Raises:
            UserManagerException: ошибка создания нового пользователя

        Returns:
            _error (List): список ошибок при создании пользователя
        """
        self.validate_password(_password)
        self.validate_login(_login)

        if len(_email) == 0:
            raise UserManagerException('Введите email')

        password = self.hash_password(_password)
        password2 = self.hash_password(_password2)
        login = _login.lower().strip()
        email = _email.lower().strip()
        role = _role
        name = _name
        email_confirmed = False

        # создаем токен для подтверждения регистрации
        token = self.create_token(email)

        # создаем новую запись
        data_store = DataStore("users")

        # проверим, что у пользователя с таким логином не существует

        if password != password2:
            raise UserManagerException("Пароли не совпадают")

        user = self.get_user_by_login(login)
        if user is not None:
            raise UserManagerException("Пользователь с таким логином уже существует")

        user = self.get_user_by_email(email)
        if user is not None:
            raise UserManagerException("Пользователь с таким email уже существует")

        # создаем новую запись
        user = User(_login=login, _name=name, _email=email, _role=role, _probationers_number=_probationers_number,
                    _token=token, _email_confirmed=email_confirmed)

        education_module_expiration_date = user.education_module_expiration_date.strftime("%d/%m/%Y")

        user_data = {"login": user.login, "password": password, "email": user.email,
                     "role": user.role, "name": user.name, "created_date": user.created_date.strftime("%d/%m/%Y"),
                     "education_module_expiration_date": education_module_expiration_date,
                     "probationers_number": user.probationers_number,
                     "active": user.active, "email_confirmed": user.email_confirmed, "token": user.token}

        return data_store.insert_row(user_data)

    def get_user_role(self, _user_id):
        """
        Возвращает роль пользователя по id

        Args:
            _id (Int): id пользователя

        Returns:
            String: роль пользователя
        """
        user = self.get_user_by_id(_user_id)
        user_role = user.role

        return user_role

    def chenge_user(self, _user_id, _login, _name, _email, _role, _probationers_number, _created_date,
                    _education_module_expiration_date="", _token="", _email_confirmed=False, _active=True):
        """
        Обновляет информацию о пользователе и возвращает ее

        Args:
            _user_id (Int): ID пользователя
            _name (String): имя пользователя
            _email (String): email пользователя
            _role (String): роль пользователя [user/superuser]
            _probationers_number (Int): максимальное количество испытуемых у пользователя
            _created_date (String): дата создания пользователя

        Returns:
            Dict: словарь с информацией о пользователе
        """
        if len(_email) == 0:
            raise UserManagerException('Введите email')

        user = self.get_user_by_email(_email)
        if user is not None:
            if user.login != _login:
                raise UserManagerException("Пользователь с таким email уже существует")

        user = User(_user_id=_user_id, _login=_login, _name=_name, _email=_email, _role=_role, _created_date=_created_date,
                    _probationers_number=_probationers_number, _token=_token, _email_confirmed=_email_confirmed,
                    _education_module_expiration_date=_education_module_expiration_date, _active=_active)

        education_module_expiration_date = user.education_module_expiration_date.strftime("%d/%m/%Y")
        user.created_date = user.created_date.strftime("%d/%m/%Y")

        data_store = DataStore("users")
        user_data = {"login": user.login, "email": user.email, "role": user.role, "name": user.name,
                     "probationers_number": user.probationers_number, "created_date": user.created_date,
                     "education_module_expiration_date": education_module_expiration_date, "active": user.active,
                     "token": user.token, "email_confirmed": user.email_confirmed}

        data_store.update_row_by_id(user_data, user.user_id)
        user = data_store.get_row_by_id(user.user_id)

        return self.user_row_to_user(user)

    def chenge_password(self, _user_id, _password, _password2, _current_password=''):
        """
        Сброс пароля пользователя

        Args:
            _user_id (Integer): ID пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _current_password(String): текущий пароль пользователя(нужен, если пароль меняет user, а не superuser).
                                        Defaults to ''
        """

        self.validate_password(_password)
        if _password != _password2:
            raise UserManagerException("введенные пароли не совпадают")

        password = self.hash_password(_password)
        data_store = DataStore("users")
        if _current_password != "":
            if _current_password is None:
                raise UserManagerException('Введите текущий пароль')
            current_password = self.hash_password(_current_password)
            user = data_store.get_row_by_id(_user_id)
            if current_password != user['password']:
                raise UserManagerException("Введенный текущий пароль неправильный")

        user_data = {"password": password}

        data_store.update_row_by_id(user_data, _user_id)

    def activation(self, _user_id):
        """
        Разблокировка пользователя

        Args:
            _user_id(Int): ID пользователя

        Returns:
            _active (bool): Активирован пользователь
        """

        user = self.get_user_by_id(_user_id)
        user.active = True

        self.chenge_user(user.user_id, user.login, user.name, user.email, user.role, user.probationers_number,
                         user.created_date, user.education_module_expiration_date,
                         user.token, user.email_confirmed, user.active)

    def deactivation(self, _user_id):
        """
        Блокировка пользователя

        Args:
            _user_id(Int): ID пользователя

        Returns:
            _active (bool): Заблокирован пользователь
        """

        user = self.get_user_by_id(_user_id)
        user.active = False

        self.chenge_user(user.user_id, user.login, user.name, user.email, user.role, user.probationers_number,
                         user.created_date, user.education_module_expiration_date,
                         user.token, user.email_confirmed, user.active)

    def access_extension(self, _period, _reference_point, _user_id):
        """
        Продление срока доступа пользователя к центру обучения

        Args:
            _period(Int): количество месяцев, на которое продлевают срок доступа пользователю
            _reference_point(String): начальное время отсчета
            _user_id(Int): ID пользователя, которому продлевают срок доступа
        """

        user = self.get_user_by_id(_user_id)

        if _reference_point == "end":
            x = relativedelta(months=_period)
            user.education_module_expiration_date = (
                    user.education_module_expiration_date + relativedelta(months=_period)).strftime("%d/%m/%Y")
        elif _reference_point == "today":
            user.education_module_expiration_date = (datetime.now() + relativedelta(months=_period)).strftime(
                "%d/%m/%Y")

        self.chenge_user(user.user_id, user.login, user.name, user.email, user.role, user.probationers_number,
                         user.created_date, user.education_module_expiration_date,
                         user.token, user.email_confirmed, user.active)
