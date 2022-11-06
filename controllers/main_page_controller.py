from services.main_page_service import MainPageService
import utils.ada as ada
from services.action_service import ActionService
from services.user_manager_service import UserManagerService
from error import UserManagerException


class MainPageController():
    """
    MainPageController - класс контроллера представления главной страницы приложения, реализующий логику взаимодейтвия приложения с пользователем
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответсвующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """ 

    def __init__(self):
        """
        Constructor
        @params:
        """

        pass

    def get_actions(self, _user_id):
        """
        Возвращает список действий, сделанных авторизованным пользователем(если авторизованный пользователь админ,
        то возвращает список действий всех пользователей, которые есть в системе)

        Args:
            _user_id(Integer): ID текущего пользователя

        Returns:
            actions(List): список испытуемых
        """

        index_service = MainPageService()
        actions_list = index_service.get_actions(_user_id)
        actions = []

        for i_action in actions_list:
            action = {}

            action["login"] = i_action["action"].user_login
            action["action"] = i_action["action"].action
            action["created_date"] = str(i_action['action'].created_date.strftime("%d/%m/%Y %H:%M:%S"))
            action['timedelta'] = i_action['timedelta']
            action['comment_action'] = i_action['action'].comment_action

            actions.append(action)


        return actions

    def get_user_view_by_user_id(self, _user_id):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)
        """

        page_service = MainPageService()

        user = page_service.get_user_by_id(_user_id)
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

        return user_view

    def chenge_password(self, _user_id, _password, _password2, _current_password):
        """
        Функция изменения пароля пользователя

        Args:
            _user_id (_type_): ID пользователя
            _password (_type_): новый пароль
            _password2 (_type_): повтор нового пароля
            _current_password (_type_): текущий пароль пользователя

        Returns:
            None: ничего не возвращает
        """        

        main_page_service = MainPageService()

        try:
            main_page_service.chenge_password(_user_id, _password, _password2, _current_password)
        except UserManagerException as error:
            return error