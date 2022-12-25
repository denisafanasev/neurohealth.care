from models.course_manager import EducationCourseManager
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

        if isinstance(error, int):
            action_manager.add_notifications(_login, "добавил", 'нового', "user_manager", login_superuser)

        return error

    def chenge_user(self, _user_id, _login, _name, _email, _role, _probationers_number, _created_date,
                    _education_module_expiration_date, _is_active,_current_user_id):
        """
        Обновляет информацию о пользователе и возвращает ее

        Args:
            _user_id(Int): ID пользователя
            _login (String): логин пользователя
            _name (String): имя пользователя
            _email (String): email пользователя
            _role (String): роль пользователя [user/superuser]
            _probationers_number(String): количество доступных тестируемых
            _created_date(String): дата создания пользователя
            _education_module_expiration_date(String): дата до которой пользователь активен
            _is_active(String): активирован/заблокирован пользователь
            _current_user_id(Int): ID текущего пользователя

        Returns:
            Dict: словарь с информацией о пользователе
        """

        user_manager = UserManager()
        action_manager = ActionManager()

        user = user_manager.chenge_user(_user_id, _login,_name, _email, _role, _probationers_number, _created_date,
                                        _education_module_expiration_date, _active=_is_active)

        login_superuser = user_manager.get_user_by_id(_current_user_id).login

        action_manager.add_notifications(user.login, "изменил", 'данные', "user_manager", login_superuser)

        return user

    def chenge_password(self, _user_id, _password, _password2, _current_user_id, _current_password=''):
        """
        Обновляет в системе пароль пользователя

        Args:
            _user_id (Integer): ID пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _current_user_id(Integer): ID текущего пользователя
            _current_password(String): текущий пароль пользователя, у которого меняют пароль

        Returns:
            String: ошибка при обновлении пароля пользователя
        """

        user_manager = UserManager()
        action_manager = ActionManager()

        error = user_manager.chenge_password(_user_id, _password, _password2, _current_password)
        login_superuser = user_manager.get_user_by_id(_current_user_id).login
        login_user = user_manager.get_user_by_id(_user_id).login

        action_manager.add_notifications(login_user, "изменил", 'пароль', "user_manager", login_superuser)

        return error

    def activation(self, _user_id, _current_user_id):
        """
        Разблокировка пользователя

        Args:
            _user_id(String): логин пользователя
            _current_user_id(Integer): ID текущего пользователя
        """

        user_manager = UserManager()
        action_manager = ActionManager()

        user_manager.activation(_user_id)
        login_user = user_manager.get_user_by_id(_user_id).login

        login_superuser = user_manager.get_user_by_id(_current_user_id).login
        action_manager.add_notifications(login_user, "изменил", 'доступ', "user_manager", login_superuser)

    def deactivation(self, _user_id, _current_user_id):
        """
        Блокировка пользователя

        Args:
            _user_id(String): логин пользователя
            _current_user_id(Integer): ID текущего пользователя
        """

        user_manager = UserManager()
        action_manager = ActionManager()

        active = user_manager.deactivation(_user_id)
        login_user = user_manager.get_user_by_id(_user_id).login

        login_superuser = user_manager.get_user_by_id(_current_user_id).login
        action_manager.add_notifications(login_user, "изменил", 'доступ', "user_manager", login_superuser)

        return active

    def get_current_user_role(self, _current_user_id):
        """
        Возвращает роль текущего пользователя

        Args:
            _current_user_id(Int): ID текущего пользователя

        Return:
            role(String): роль текущего пользователя
        """

        user_manager = UserManager()

        return user_manager.get_user_by_id(_current_user_id).role

    def access_extension(self, _period, _reference_point, _user_id, _current_user_id):
        """
        Продление срока доступа пользователя к центру обучения

        Args:
            _period(Int): количество месяцев, на которое продлевают срок доступа пользователю
            _reference_point(String): начальное время отсчета
            _user_id(Int): ID пользователя, которому продлевают срок доступа
            _current_user_id(Int): ID текущего пользователя
        """
        user_manager = UserManager()
        action_manager = ActionManager()

        user_manager.access_extension(_period, _reference_point, _user_id)
        login_superuser = user_manager.get_user_by_id(_current_user_id).login
        login_user = user_manager.get_user_by_id(_user_id).login

        action_manager.add_notifications(login_user, "продлил", 'срок доступа', "user_manager", login_superuser)

    def get_education_streams_list(self, _user_id, _role_user):
        """
        Возвращает список обучающих потоков, в которых есть пользователя

        Args:
            _user_id(Int): ID пользователя
            _role_user(String): роль пользователя [user/superuser]

        Returns:
            List(EducationStream): список обучающих потоков
        """
        education_stream_manager = EducationStreamManager()
        user_manager = UserManager()
        course_manager = EducationCourseManager()

        education_streams = education_stream_manager.get_education_streams_list_by_id_user(_user_id, _role_user)
        if _role_user == 'superuser':
            education_streams.extend(education_stream_manager.get_education_streams_by_teacher(_user_id))

        education_streams_list = []
        for education_stream in education_streams:
            education_stream.teacher = user_manager.get_user_by_id(education_stream.teacher).name
            education_stream.course = course_manager.get_course_by_id(education_stream.course).name
            education_streams_list.append(education_stream)

        return education_streams_list