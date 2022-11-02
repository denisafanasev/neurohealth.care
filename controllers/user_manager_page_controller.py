import utils.ada as ada
from services.user_manager_service import UserManagerService
from error import UserManagerException
import config


class UserManagerPageController():
    """
    UserManagerPageController - класс контроллера представления управления списком пользователей системы
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответсвующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_users_list_view(self, _user_id):
        """
        Возвращает отформатированный список пользователей

        Returns:
            List: список пользователей, каждый из которых представлен структурой типа Dict
        """ 

        user_manager_service = UserManagerService()
        users = user_manager_service.get_users(_user_id)

        users_list_view = []
        for user in users:

            user_view = {}

            user_view['user_id'] = user.user_id
            user_view['login'] = user.login
            user_view['name'] = user.name
            user_view['email'] = user.email
            user_view['role'] = user.role
            user_view['created_date'] = str(user.created_date.strftime("%d/%m/%Y"))
            user_view['education_module_expiration_date'] = str(user.education_module_expiration_date.strftime("%d/%m/%Y"))
            user_view['probationers_number'] = user.probationers_number
            user_view['is_active'] = user.active
            user_view['active_education_module'] = user.active_education_module
            user_view['email_confirmed'] = user.email_confirmed

            users_list_view.append(user_view)
            
        return users_list_view

    def get_users_profile_view(self, _user_id):
        """
        Возвращает представление профиля пользователя

        Returns:
            Dict: характеристики профиля пользователя
        """

        user_manager_service = UserManagerService()

        user = user_manager_service.get_users_profile(_user_id)

        user_view = {}
        if user is not None:
            user_view['user_id'] = user.user_id
            user_view['login'] = user.login
            user_view['name'] = user.name
            user_view['email'] = user.email
            user_view['role'] = user.role

            user_view['created_date'] = str(user.created_date.strftime("%d/%m/%Y"))
            user_view['education_module_expiration_date'] = str(user.education_module_expiration_date.strftime("%d/%m/%Y"))

            user_view['probationers_number'] = user.probationers_number
            user_view['token'] = user.token
            user_view['education_stream_list'] = []

            '''
            if user.role == "user":
                for education_stream in user.education_stream_list:
                    user_view['education_stream_list'].append({
                        "name": education_stream.name,
                        "teacher": education_stream.teacher,
                        "date_start": education_stream.date_start.strftime("%d/%m/%Y"),
                        "date_end": education_stream.date_end.strftime("%d/%m/%Y"),
                        "course": education_stream.course.name,
                        "status": education_stream.status
                    })
            '''

            user_view['active'] = user.active
        else:
            user_view["login"] = "введите логин пользователя.."
            user_view["name"] = "введите имя пользователя.."
            user_view["email"] = "введите email пользователя.."
            user_view["password"] = "введите пароль.."
            user_view["password2"] = "введите повторно пароль.."
            user_view["role"] = "Выберите роль пользователя"
            user_view["probationers_number"] = "Выберите количество доступных тестируемых"
            user_view["token"] = ""
            user_view["active"] = True
            user_view["email_confirmed"] = False

        return user_view

    def create_user(self, _login, _name, _password, _password2, _email, _role, _probationers_number, _current_user_id):
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

        Returns:
            String: ошибка при создании пользователя

        """

        user_manager_service = UserManagerService()
        try:
            user_manager_service.create_user(_login, _name, _password, _password2, _email, _role,
                                            _probationers_number, _current_user_id)
        except UserManagerException as error:
            return error

    def chenge_user(self, _login, _name, _email, _role, _probationers_number, _created_date,
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

        user_manager_service = UserManagerService()

        user_manager_service.chenge_user(_login, _name, _email, _role, _probationers_number, _created_date,
                                         _education_module_expiration_date, _current_user_id)

        error = "Изменения успешно сохранены!"

        return error

    def chenge_password(self, _login, _password, _password2, _current_user_id):
        """
        Обновляет в системе пароль пользователя

        Args:
            _login (String): логин пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя

        Returns:
            String: ошибка при обновлении пароля пользователя
        """

        user_manager_service = UserManagerService()
        try:
            user_manager_service.chenge_password(_login, _password, _password2, _current_user_id)
        except UserManagerException as error:

            return error

        return "Пароль успешно изменен!"

    def activation(self, _login, _current_user_id):
        """
        разблокировка пользователя

        Args:
            _login(String): логин пользователя

        Returns:
            _active (bool): Активирован/заблокирован пользователь
        """

        user_manager_service = UserManagerService()

        user_manager_service.activation(_login, _current_user_id)

        return "Пользователь успешно разблокирован!"
    
    def deactivation(self, _login, _current_user_id):
        """
        Блокировка пользователя

        Args:
            _login(String): логин пользователя

        Returns:
            _active (bool): Активирован/заблокирован пользователь
        """

        user_manager_service = UserManagerService()

        user_manager_service.deactivation(_login, _current_user_id)

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

    def access_extension(self, _period, _reference_point, _login, _current_user_id):
        """
        Продление доступа пользователя к центру обучения

        Args:
            _period(Int): количество месяцев
            _reference_point(String): точка отсчета
            _login(String): логин пользователя
        """

        user_manager_service = UserManagerService()

        user_manager_service.access_extension(_period, _reference_point, _login, _current_user_id)
        error = "Доступ пользователя к обучающей программе успешно изменен!"

        return error
