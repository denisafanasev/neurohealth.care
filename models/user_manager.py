import hashlib

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
        
            user = User(user_data.doc_id, user_data['login'], user_data['name'], user_data['email'], user_data['role']) 

        return user

    def get_user(self, _login, _password):
        """
        Возвращает id  пользователя по логину и паролю

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
            user = User(user_data[0].doc_id, user_data[0]['login'], user_data[0]['name'], user_data[0]['email'], user_data[0]['role'])
        
        return user

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

        user = self.get_user(login, password)

        if user is not None:
            raise UserManagerException("Пользователь с таким логином уже существует")
        
        # создаем новую запись
        user_data = {"login": login, "password": password, "email": email, "role": role, "name": name}
        user_id = data_store.add_row(user_data)