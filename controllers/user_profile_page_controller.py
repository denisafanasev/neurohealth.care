from services.user_profile_service import UserProfileService
from error import UserManagerException

class UserProfilePageController():

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_users_profile_view(self, _user_id):
        """
        Возвращает представление профиля пользователя

        Returns:
            Dict: характеристики профиля пользователя
        """        

        user_profile_service = UserProfileService()

        user = user_profile_service.get_users_profile(_user_id)

        user_view = {}
        if user is not None:
            user_view['user_id'] = user.user_id
            user_view['login'] = user.login
            user_view['name'] = user.name
            user_view['email'] = user.email
            user_view['role'] = user.role
            user_view['access_time'] = user.access_time

            user_view['created_date'] = str(user.created_date.strftime("%d/%m/%Y"))
            if not user.expires_date == "неограниченно":
                user_view['expires_date'] = str(user.expires_date.strftime("%d/%m/%Y"))
            else:
                user_view['expires_date'] = user.expires_date

            user_view['probationers_number'] = user.probationers_number
            user_view['token'] = user.token

            user_view['is_active'] = user.active
        else:

            user_view["login"] = "введите логин пользователя.."
            user_view["name"] = "введите имя пользователя.."
            user_view["email"] = "введите email пользователя.."
            user_view["password"] = "введите пароль.."
            user_view["password2"] = "введите повторно пароль.."
            user_view["role"] = "Выберите роль пользователя"
            user_view["probationers_number"] = "Выберите количество доступных тестируемых"
            user_view["access_time"] = "Выберите срок предоставления доступа"
            user_view["token"] = ""
            user_view["is_active"] = True
            user_view["email_confirmed"] = False

        return user_view

    def create_user(self, _login, _name, _password, _password2, _email, _role, _probationers_number, _access_time):
        """
        Создает в системе пользователя

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
            String: ошибка при создании пользователя

        """

        user_profile_service = UserProfileService()
        try:
            user_profile_service.create_user(_login, _name, _password, _password2, _email, _role,
                                            _probationers_number, _access_time)
        except UserManagerException as error:
            return error

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

        user_profile_service = UserProfileService()

        return user_profile_service.change_user(_login, _name, _email, _role, _probationers_number, _access_time,
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

        user_profile_service = UserProfileService()
        try:
            user_profile_service.discharge_password(_login, _password, _password2)
        except UserManagerException as error:

            return error

    def activation_deactivation(self, _login):
        """
        Блокировка/разблокировка пользователя

        Args:
            _login(String): логин пользователя

        Returns:
            _active (bool): Активирован/заблокирован пользователь
        """

        user_profile_service = UserProfileService()

        return user_profile_service.activation_deactivation(_login)

    def get_settings_user(self):
        """
        Возвращает возможные настройки пользователя

        Returns:
            settings_user (Dict): словарь с настройками
        """

        user_profile_service = UserProfileService()

        return user_profile_service.get_settings_user()
