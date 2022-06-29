from models.user_manager import UserManager
from services.action_service import ActionService
# from services.user_profile_service import UserProfileService
from services import learning_stream_service

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
        stream_service = learning_stream_service.LearningStreamService()

        if _login_user == "":
            user = user_manager.get_user_by_id(user_manager.get_current_user_id())
        else:
            user = user_manager.get_user_by_login(_login_user)

        if user is not None:

            user.learning_stream_list = stream_service.get_learning_streams_list_by_login_user(user.login, user.role)


        return user

    def get_users_profile(self, user_id):
        """
        Возвращает представление профиля пользователя

        Returns:
            Dict: характеристики профиля пользователя
        """

        user_manager = UserManager()
        # user_profile_service = UserProfileService()
        stream_service = learning_stream_service.LearningStreamService()

        user = user_manager.get_user_by_id(user_id)

        if user is not None:
            if user.role == "user":
                learning_stream_list = []
                for id_learning_stream in user.learning_stream_list:
                    learning_stream_list.append(stream_service.get_learning_stream(id_learning_stream))
                user.learning_stream_list = learning_stream_list
            else:
                user.learning_stream_list = None

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

        active = None

        if not _active:
            active = user_manager.activation(_login)
        elif _active:
            active = user_manager.deactivation(_login)

        login_superuser = self.get_current_user('').login

        ActionService().add_notifications(_login, "overwrite", 'доступ', "user_manager", login_superuser)

        return active

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

    # def add_user_in_learning_stream(self, _id_learning_stream, _users_list):
    #     """
    #     Добавляет пользователей к обучающему потоку
    #
    #     Args:
    #         _id_learning_stream(Int): идентификатор обучающего потока
    #         _users_list(List): список пользователей
    #     """
    #
    #     user_manager = UserManager()
    #
    #     return user_manager.add_user_in_learning_stream(_id_learning_stream, _users_list)
    #
    # def exclusion_of_users_from_list(self, _excluded_users_list, _id_learning_stream):
    #     """
    #     Исключает пользователей из обучающего потока
    #
    #     Args:
    #         _id_learning_stream(Int): идентификатор обучающего потока
    #         _excluded_users_list(List): список пользователей
    #     """
    #
    #     user_manager = UserManager()
    #
    #     user_manager.exclusion_of_users_from_list(_excluded_users_list, _id_learning_stream)