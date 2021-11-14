import hashlib
import flask_login
from datetime import datetime


from models.user import User
from data_adapters.data_store import DataStore

from error import UserManagerException

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
    
    def validate_password(self, _password):
        """
        Проверка пароля на корректное значение

        Args:
            _password (String): пароль

        Raises:
            UserManagerException: ошибка корректности значения пароля
        """        

        if (len(_password) < 4) or (len(_password)>20):
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

        if (len(_login) < 3) or (len(_login)>10):
            raise UserManagerException("неверная длинная логина пользователя, укажите минимум 4 символа и максимум 10")

    def user_row_to_user(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о пользователи в структуру User

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            User: пользователь
        """        

        # создадим пользователя с указанием обязательных атрибутов
        user = User(_data_row.doc_id, _data_row['login'], _data_row['name'], _data_row['email'], _data_row['role'])

        # проверим наличие в структуре хранения необязательных атрибутов
        if _data_row.get('probationers_number') is not None:
                user.probationers_number = int(_data_row['probationers_number'])
        
        if _data_row.get('created_date') is not None:
                user.created_date = datetime.strptime(_data_row['created_date'], '%d/%m/%Y')

        if _data_row.get('expires_date') is not None:
                user.expires_date = datetime.strptime(_data_row['expires_date'], '%d/%m/%Y')

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

        return user

    def get_user(self, _login, _password):
        """
        Возвращает пользователя по логину и паролю

        Args:
            _login   - Required  : current iteration (String)
            _password   - Required  : current iteration (String)
        """

        user = None

        login = _login.lower()
        password = self.hash_password(_password)

        data_store = DataStore("users")

        user_data = data_store.get_rows({"login": login, "password": password})

        if len(user_data) > 1:
            raise UserManagerException("Ошибка в базе данных пользователей")
        
        if len(user_data) == 1:
            user = self.user_row_to_user(user_data[0])
        
        return user
    
    def get_user_by_login(self, _login):
        """
        Возвращает пользователя по логину

        Args:
            _login   - Required  : current iteration (String)
        """

        user = None

        login = _login.lower()
        data_store = DataStore("users")

        user_data = data_store.get_rows({"login": login})

        if len(user_data) > 1:
            raise UserManagerException("Ошибка в базе данных пользователей")
        
        if len(user_data) == 1:
            user = self.user_row_to_user(user_data[0])
        
        return user
    
    def get_users(self):
        """
        Возвращает список пользователей в системе, в соответсвии с ролью пользователя, который запрашивает список

        Args:
            None

        Returns:
            List: список пользователей с типом User
        """

        users = []

        data_store = DataStore("users")

        users_list_data = data_store.get_rows()

        for user_data in users_list_data:
    
            #user = User(user_data.doc_id, user_data['login'], user_data['name'], user_data['email'], user_data['role'])
            user = self.user_row_to_user(user_data)
            
            if self.get_user_role(self.get_current_user_id()) == "superuser":
                users.append(user)
            else:
                if self.get_current_user_id() == user.id:
                    users.append(user)

        return users
        

    def is_there_users(self):
        """
        Проверяем, есть ли в системе пользователи

        Args:
            None
        """

        data_store = DataStore("users")

        data = data_store.get_rows_count()

        if data != 0:
            return True
        
        return False
    
    def create_user(self, _login, _name, _password, _password2, _email, _role):
        """
        Процедура создания нового пользователя в системе

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _email (String): email пользователя
            _role (String): роль пользователя [user/superuser]

        Raises:
            UserManagerException: ошибка создания нового пользователя
        """             

        self.validate_login(_login)
        self.validate_password(_password)
        self.validate_role(_role)

        if _password != _password2:
            raise UserManagerException("введенные пароли не совпадают")

        password = self.hash_password(_password)
        login = _login.lower()
        email = _email.lower()
        role = _role
        name = _name

        # создаем новую запись
        data_store = DataStore("users")

        # проверим, что тпользователя с таким логином не существует

        user = self.get_user_by_login(login)

        if user is not None:
            raise UserManagerException("Пользователь с таким логином уже существует")
        
        # создаем новую запись
        user = User(_login=login, _name=name, _email=email, _role=role)

        user_data = {"login": user.login, "password": password, "email": user.email, 
                     "role": user.role, "name": user.name, "created_date": user.created_date.strftime("%d/%m/%Y"), 
                     "expires_date": user.expires_date.strftime("%d/%m/%Y"), "probationers_number": user.probationers_number}

        data_store.add_row(user_data)
    
    def get_current_user_id(self):
        """
        Возвращает id текущего авторизованного пользователя

        Returns:
            Int: id пользователя
        """        
        
        id = None

        if flask_login.current_user.is_authenticated:
            id = flask_login.current_user.user_id
        
        return id
    
    def get_user_role(self, _id):
        """
        Возвращает роль пользователя по id

        Args:
            _id (Int): id пользователя

        Returns:
            String: роль пользователя
        """        

        user_id = self.get_current_user_id()
        user = self.get_user_by_id(user_id)
        user_role = user.role

        return user_role
