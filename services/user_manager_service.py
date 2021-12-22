from models.user_manager import UserManager

class UserManagerService():
    """
    UserManagerService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_users(self):
        """
        Возвращает список пользователей

        Returns:
            List: список пользователей с типом User
        """        

        users = []

        user_manager = UserManager()
        users = user_manager.get_users()

        return users
    
    def create_user(self, _login, _name, _password, _password2, _email, _role, _probationers_number, _access_time):
        """
        Создает в системе суперпользователя

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _email (String): email пользователя
            _role (String): роль пользователя [user/superuser]
            _probationers_number (int): количество доступных тестируемых
            _access_time (String): срок доступа

        Returns:
            List: список ошибок при создании пользователя

        """

        user_manager = UserManager()
        user_manager.create_user(_login, _name, _password, _password2, _email, _role, _probationers_number, _access_time)

    def change_user(self, _login, _name, _email, _role, _probationers_number, _access_time, _created_date):
        """
        Обновляет информацию о пользователе и возвращает ее

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _email (String): email пользователя
            _role (String): роль пользователя [user/superuser]
            _access_time (String): срок доступа

        Returns:
            Dict: словарь с информацией о пользователе
        """

        user_manager = UserManager()

        return user_manager.change_user(_login, _name, _email, _role, _probationers_number, _access_time, _created_date)

    def discharge_password(self, _login, _password, _password2):
        """

        """

        user_manager = UserManager()

        return user_manager.discharge_password(_login, _password, _password2)