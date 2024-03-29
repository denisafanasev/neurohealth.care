import config
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

            user_view['created_date'] = str(user.created_date.strftime("%d/%m/%Y"))
            user_view['education_module_expiration_date'] = str(
                user.education_module_expiration_date.strftime("%d/%m/%Y"))

            user_view['probationers_number'] = user.probationers_number
            user_view['token'] = user.token
            user_view['education_stream_list'] = []

            user_view['active'] = user.active

        data_placeholder = {
            "login": "введите логин пользователя..",
            "name": "введите имя пользователя..",
            "email": "введите email пользователя..",
            "password": "введите пароль..",
            "password2": "введите повторно пароль..",
            "role": "Выберите роль пользователя",
            "probationers_number": "Выберите количество доступных тестируемых",
            "token": "",
            "active": True,
            "email_confirmed": False}

        return user_view, data_placeholder

    def create_user(self, _user, _current_user_id):
        """
        Создает в системе пользователя. Если нет ошибок при создании пользователя, возвращает id нового пользователя,
        иначе передает сообщение ошибки.

        Args:
            _user (Dict): данные нового пользователя
            _current_user_id(Int): ID текущего пользователя

        Returns:
            String: ошибка при создании пользователя
        """

        user_profile_service = UserProfileService()
        try:
            user_id = user_profile_service.create_user(_user, _current_user_id=_current_user_id)
        except UserManagerException as error:
            return error

        return user_id

    def chenge_user(self, _user_id, _user, _current_user_id):
        """
        Обновляет информацию о пользователе и возвращает ее

        Args:
            _user (Dict): обновленные данные пользователя
            _current_user_id(Int): ID текущего пользователя
            _user_id(Int): ID пользователя, чьи данные обновляют

        Returns:
            Dict: словарь с информацией о пользователе
        """

        user_profile_service = UserProfileService()

        try:
            user_profile_service.chenge_user(_user_id, _user, _current_user_id)

        except UserManagerException as error:
            return error

    def chenge_password(self, _user_id, _password, _password2, _current_user_id):
        """
        Обновляет в системе пароль пользователя

        Args:
            _user_id (Integer): ID пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _current_user_id(Integer): ID текущего пользователя

        Returns:
            String: ошибка при обновлении пароля пользователя
        """

        user_profile_service = UserProfileService()
        try:
            user_profile_service.chenge_password(_user_id, _password, _password2, _current_user_id)
        except UserManagerException as error:
            return error, 'Error'

        return "Пароль успешно изменен!", 'Successful'

    def activation(self, _user_id, _current_user_id):
        """
        разблокировка пользователя

        Args:
            _user_id(String): логин пользователя

        Returns:
            _active (bool): Активирован/заблокирован пользователь
        """

        user_profile_service = UserProfileService()

        user_profile_service.activation(_user_id, _current_user_id)

        return "Пользователь успешно разблокирован!"

    def deactivation(self, _user_id, _current_user_id):
        """
        Блокировка пользователя

        Args:
            _user_id(String): логин пользователя

        Returns:
            _active (bool): Активирован/заблокирован пользователь
        """

        user_profile_service = UserProfileService()

        user_profile_service.deactivation(_user_id, _current_user_id)

        return "Пользователь успешно заблокирован!"

    def get_settings_user(self):
        """
        Возвращает возможные настройки пользователя

        Returns:
            settings_user (Dict): словарь с настройками
        """

        settings_user = {
            "role": config.ROLE,
            "probationers_number": config.PROBATIONERS_NUMBER,
            "education_module_expiration_date": config.EDUCATION_MODULE_EXPIRATION_DATE,
            "reference_point": config.REFERENCE_POINT
        }

        return settings_user

    def access_extension(self, _period, _reference_point, _user_id, _current_user_id):
        """
        Продление доступа пользователя к центру обучения

        Args:
            _period(Int): количество месяцев
            _reference_point(String): точка отсчета
            _user_id(Int): ID пользователя
            _current_user_id(Int): ID текущего пользователя
        """

        user_profile_service = UserProfileService()

        user_profile_service.access_extension(_period, _reference_point, _user_id, _current_user_id)
        error = "Доступ пользователя к обучающей программе успешно изменен!"

        return error

    def get_education_streams_list(self, _user_id, _role_user):
        """
        Возвращает список обучающих потоков, в которых находится данный пользователь

        Args:
            _user_id(Int): ID пользователя
            _role_user(String): роль пользователя

        Returns:
            List(EducationStream): список обучающих потоков
        """
        user_profile_service = UserProfileService()

        education_streams_list = user_profile_service.get_education_streams_list(_user_id, _role_user)
        role_selected_user = ''
        if _role_user == 'user':
            role_selected_user = 'учащийся'

        education_streams_list_view = []
        for education_stream in education_streams_list:
            if _role_user == 'superuser':
                if _user_id == education_stream.teacher.user_id:
                    role_selected_user = 'учитель'
                else:
                    role_selected_user = 'куратор'

            education_stream_view = {
                'id': education_stream.id,
                'name': education_stream.name,
                'course': education_stream.course,
                'date_start': education_stream.date_start.strftime('%d/%m/%Y'),
                'date_end': education_stream.date_end.strftime('%d/%m/%Y'),
                'teacher': education_stream.teacher.name,
                'status': education_stream.status,
                'role_selected_user': role_selected_user
            }

            education_streams_list_view.append(education_stream_view)

        return education_streams_list_view

