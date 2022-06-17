from models.user_manager import UserManager
from services.action_service import ActionService


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

    def get_current_user(self, _login_user):
        """
        Возвращает модель User пользователя. Если _login_user = '', то возвращает модель User текущего пользователя

        Args:
            _login_user: логин пользователя

        Returns:
            user(User): модель User
        """

        user_manager = UserManager()

        if _login_user == "":
            return user_manager.get_user_by_id(user_manager.get_current_user_id())
        else:
            return user_manager.get_user_by_login(_login_user)

    def get_users_profile(self, user_id):
        """
        Возвращает представление профиля пользователя

        Returns:
            Dict: характеристики профиля пользователя
        """
        user_manager = UserManager()
        user = user_manager.get_user_by_id(user_id)
        return user

    def create_user(self, _login, _name, _password, _password2, _email, _role, _probationers_number):
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

        Returns:
            List: список ошибок при создании пользователя
        """

        user_manager = UserManager()

        error = user_manager.create_user(_login, _name, _password, _password2, _email, _role, _probationers_number)
        login_superuser = self.get_current_user('').login

        if error is None:
            ActionService().add_notifications(_login, "add", 'нового', "user_manager", login_superuser)

        return error

    def change_user(self, _login, _name, _email, _role, _probationers_number, _created_date, _education_module_expiration_date):
        """
        Обновляет информацию о пользователе и возвращает ее

        Args:
            _login (String): логин пользователя
            _name (String): имя пользователя
            _email (String): email пользователя
            _role (String): роль пользователя [user/superuser]

        Returns:
            Dict: словарь с информацией о пользователе
        """

        user_manager = UserManager()

        user = user_manager.change_user(_login, _name, _email, _role, _probationers_number, _created_date,
                                 _education_module_expiration_date)
        login_superuser = self.get_current_user('').login

        ActionService().add_notifications(_login, "overwrite", 'данные', "user_manager", login_superuser)

        return user

    def discharge_password(self, _login, _password, _password2, _current_password=''):
        """
        Обновляет в системе пароль пользователя

        Args:
            _login (String): логин пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя

        Returns:
            String: ошибка при обновлении пароля пользователя
        """

        user_manager = UserManager()

        error = user_manager.discharge_password(_login, _password, _password2, _current_password)
        login_superuser = self.get_current_user('').login

        ActionService().add_notifications(_login, "overwrite", 'пароль', "user_manager", login_superuser)

        return error

    def activation_deactivation(self, _login, _active):
        """
        Блокировка/разблокировка пользователя

        Args:
            _login(String): логин пользователя

        Returns:
            _active (bool): Активирован/заблокирован пользователь
        """

        user_manager = UserManager()

        if not _active:
            user_manager.activation(_login)
        elif _active:
            user_manager.deactivation(_login)

        login_superuser = self.get_current_user('').login

        ActionService().add_notifications(_login, "overwrite", 'доступ', "user_manager", login_superuser)

    def get_current_user_role(self):
        """
        Возвращает роль текущего пользователя

        Return:
            role(String): роль текущего пользователя
        """

        user_manager = UserManager()

        return user_manager.get_user_by_id(user_manager.get_current_user_id()).role

    def access_extension(self, _period, _reference_point, _login):
        """
        Ппродление срока доступа пользователя к центру обучения

        Args:
            _period(Int): количество месяцев, на которое продлевают срок доступа пользователю
            _reference_point(String): начальное время отсчета
            _login(String): логин пользователя, которому продлевают срок доступа
        """
        user_manager = UserManager()

        user_manager.access_extension(_period, _reference_point, _login)
        login_superuser = self.get_current_user('').login

        ActionService().add_notifications(_login, "extended", 'срок доступа', "user_manager", login_superuser)
