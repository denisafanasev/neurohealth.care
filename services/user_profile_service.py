from models.user_manager import UserManager
from services.action_service import ActionService


class UserProfileService():

    def init(self):
        pass

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

        ActionService().add_notifications(_login, "add", "user_manager")

        return user_manager.create_user(_login, _name, _password, _password2, _email, _role, _probationers_number)

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

        ActionService().add_notifications(_login, "overwrite", "user_manager")

        return user_manager.change_user(_login, _name, _email, _role, _probationers_number, _created_date, _education_module_expiration_date)

    def discharge_password(self, _login, _password, _password2):
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

        user_manager.discharge_password(_login, _password, _password2)

        ActionService().add_notifications(_login, "overwrite", "user_manager")

    def activation_deactivation(self, _login, _active):
        """
        Блокировка/разблокировка пользователя

        Args:
            _login(String): логин пользователя

        Returns:
            _active (bool): Активирован/заблокирован пользователь
        """

        user_manager = UserManager()

        ActionService().add_notifications(_login, "overwrite", "user_manager")

        if not _active:
            return user_manager.activation(_login)
        elif _active:
            return user_manager.deactivation(_login)

    def get_current_user_role(self):

        user_manager = UserManager()

        return user_manager.get_user_by_id(user_manager.get_current_user_id())

    def access_extension(self, _period, _reference_point, _login):

        user_manager = UserManager()

        return user_manager.access_extension(_period, _reference_point, _login)