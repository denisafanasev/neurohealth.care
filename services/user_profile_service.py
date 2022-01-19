from models.user_manager import UserManager


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

        return user_manager.create_user(_login, _name, _password, _password2, _email, _role, _probationers_number, _access_time)

    def change_user(self, _login, _name, _email, _role, _probationers_number, _access_time, _created_date, _active):
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

        return user_manager.change_user(_login, _name, _email, _role, _probationers_number, _access_time,
                                        _created_date, _active)

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

        return user_manager.discharge_password(_login, _password, _password2)

    def activation_deactivation(self, _login):
        """
        Блокировка/разблокировка пользователя

        Args:
            _login(String): логин пользователя

        Returns:
            _active (bool): Активирован/заблокирован пользователь
        """

        user_manager = UserManager()

        return user_manager.activation_deactivation(_login)
