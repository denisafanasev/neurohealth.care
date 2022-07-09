from models.user_manager import UserManager
from models.action_manager import ActionManager
from models.education_stream_manager import EducationStreamManager


class UserProfileService():
    """
    UserProfileService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

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

    def create_user(self, _login, _name, _password, _password2, _email, _role, _probationers_number, _user_id):
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
        action_manager = ActionManager()

        login_superuser = user_manager.get_user_by_id(_user_id).login

        action_manager.add_notifications(_login, "добавил", '', "user_manager", login_superuser)

        return user_manager.create_user(_login, _name, _password, _password2, _email, _role, _probationers_number)

    def change_user(self, _login, _name, _email, _role, _probationers_number, _created_date,
                    _education_module_expiration_date):
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
        action_manager = ActionManager()

        action_manager.add_notifications(_login, "изменил", '', "user_manager", _login)

        return user_manager.change_user(_login, _name, _email, _role, _probationers_number, _created_date,
                                        _education_module_expiration_date)

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
        action_manager = ActionManager()

        user_manager.discharge_password(_login, _password, _password2)

        action_manager.add_notifications(_login, "изменил", '', "user_manager", _login)

    def activation_deactivation(self, _login, _active):
        """
        Блокировка/разблокировка пользователя

        Args:
            _login(String): логин пользователя

        Returns:
            _active (bool): Активирован/заблокирован пользователь
        """

        user_manager = UserManager()
        action_manager = ActionManager()

        action_manager.add_notifications(_login, "изменил", '', "user_manager", _login)

        if not _active:
            return user_manager.activation(_login)
        elif _active:
            return user_manager.deactivation(_login)

    def get_current_user(self, _login_user, _user_id):
        """
        Возвращает модель User пользователя. Если _login_user = '', то возвращает модель User текущего пользователя

        Args:
            _login_user: логин пользователя

        Returns:
            user(User): модель User
        """

        user_manager = UserManager()

        if _login_user == "":
            return user_manager.get_user_by_id(user_manager.get_user_by_id(_user_id))
        else:
            return user_manager.get_user_by_login(_login_user)

    def access_extension(self, _period, _reference_point, _login):
        """
        Ппродление срока доступа пользователя к центру обучения

        Args:
            _period(Int): количество месяцев, на которое продлевают срок доступа пользователю
            _reference_point(String): начальное время отсчета
            _login(String): логин пользователя, которому продлевают срок доступа
        """

        user_manager = UserManager()

        return user_manager.access_extension(_period, _reference_point, _login)

    def get_education_streams_users(self, _education_stream_list):
        """
        Возвращает список обучающих потоков по id, в которых есть пользователь

        Args:
            _education_stream_list(List): список id обучающих потоков

        Returns:
            (List): список обучающих потоков
        """

        education_stream_manager = EducationStreamManager()

        education_stream_list = []
        for education_stream in _education_stream_list:
            education_stream_list.append(education_stream_manager.get_education_stream(education_stream))

        return education_stream_list

