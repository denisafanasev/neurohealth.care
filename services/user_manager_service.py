from models.user_manager import UserManager
from models.education_stream_manager import EducationStreamManager
from models.action_manager import ActionManager

class UserManagerService():
    """
    UserManagerService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """ 

    def init(self):
        pass

    def get_users(self, _user_id):
        """
        Возвращает список пользователей

        Returns:
            List: список пользователей с типом User
        """        

        users = []

        user_manager = UserManager()
        users = user_manager.get_users(_user_id)

        return users

    def get_user_by_login(self, _login_user):
        """
        Возвращает модель User пользователя. Если _login_user = '', то возвращает модель User текущего пользователя

        Args:
            _login_user: логин пользователя

        Returns:
            user(User): модель User
        """

        user_manager = UserManager()
        #stream_service = education_stream_service.EducationStreamService()

        #if _login_user == "":
        #    user = user_manager.get_user_by_id(user_manager.get_current_user_id())
        #else:
        
        user = user_manager.get_user_by_login(_login_user)

        #if user is not None:
        #    user.education_stream_list = stream_service.get_education_streams_list_by_login_user(user.login, user.role)


        return user

    def get_users_profile(self, user_id):
        """
        Возвращает представление профиля пользователя

        Returns:
            Dict: характеристики профиля пользователя
        """

        user_manager = UserManager()
        stream_manager = EducationStreamManager()

        user = user_manager.get_user_by_id(user_id)

        if user is not None:
            if user.role == "user":
                education_stream_list = []
                for id_education_stream in user.education_stream_list:
                    education_stream_list.append(
                        stream_manager.get_education_stream(id_education_stream))
                user.education_stream_list = education_stream_list
            else:
                user.education_stream_list = None

        return user

    def create_user(self, _login, _name, _password, _password2, _email, _role, _probationers_number, _current_user_id):
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

        error = user_manager.create_user(_login, _name, _password, _password2, _email, _role, _probationers_number)
        login_superuser = user_manager.get_user_by_id(_current_user_id).login

        if error is None:
            action_manager.add_notifications(_login, "добавил", 'нового', "user_manager", login_superuser)

        return error

    def change_user(self, _login, _name, _email, _role, _probationers_number, _created_date,
                    _education_module_expiration_date, _current_user_id):
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

        user = user_manager.change_user(_login, _name, _email, _role, _probationers_number, _created_date,
                                 _education_module_expiration_date)

        login_superuser = user_manager.get_user_by_id(_current_user_id).login

        action_manager.add_notifications(_login, "изменил", 'данные', "user_manager", login_superuser)

        return user

    def discharge_password(self, _login, _password, _password2, _current_user_id, _current_password=''):
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

        error = user_manager.discharge_password(_login, _password, _password2, _current_password)
        login_superuser = user_manager.get_user_by_id(_current_user_id).login

        action_manager.add_notifications(_login, "изменил", 'пароль', "user_manager", login_superuser)

        return error

    def activation(self, _login, _current_user_id):
        """
        разблокировка пользователя

        Args:
            _login(String): логин пользователя
        """

        user_manager = UserManager()
        action_manager = ActionManager()

        user_manager.activation(_login)

        login_superuser = user_manager.get_user_by_id(_current_user_id).login
        action_manager.add_notifications(_login, "изменил", 'доступ', "user_manager", login_superuser)


    def deactivation(self, _login, _current_user_id):
        """
        Блокировка пользователя

        Args:
            _login(String): логин пользователя
        """

        user_manager = UserManager()
        action_manager = ActionManager()

        active = user_manager.deactivation(_login)

        login_superuser = user_manager.get_user_by_id(_current_user_id).login
        action_manager.add_notifications(_login, "изменил", 'доступ', "user_manager", login_superuser)

        return active

    def get_current_user_role(self, _current_user_id):
        """
        Возвращает роль текущего пользователя

        Return:
            role(String): роль текущего пользователя
        """

        user_manager = UserManager()

        return user_manager.get_user_by_id(_current_user_id).role


    def access_extension(self, _period, _reference_point, _login, _current_user_id):
        """
        Ппродление срока доступа пользователя к центру обучения

        Args:
            _period(Int): количество месяцев, на которое продлевают срок доступа пользователю
            _reference_point(String): начальное время отсчета
            _login(String): логин пользователя, которому продлевают срок доступа
        """
        user_manager = UserManager()
        action_manager = ActionManager()

        user_manager.access_extension(_period, _reference_point, _login)
        login_superuser = user_manager.get_user_by_id(_current_user_id).login

        action_manager.add_notifications(_login, "продлил", 'срок доступа', "user_manager", login_superuser)
