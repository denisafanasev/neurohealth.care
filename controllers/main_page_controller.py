import utils.ada as ada
from services.action_service import ActionService


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

    def get_actions(self):
        """
        Возвращает список действий, сделанных авторизованным пользователем(если авторизованный пользователь админ,
        то возвращает список действий всех пользователей, которые есть в системе)

        Returns:
            actions(List): список испытуемых
        """

        index_service = ActionService()
        actions_list = index_service.get_actions()
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

    def get_current_user(self):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)
        """

        index_service = ActionService()

        user = index_service.get_current_user()
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