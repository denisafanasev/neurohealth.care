from models.action_manager import ActionManager


class ActionService():
    """
    ActionService - класс бизнес-логики сервиса управления системными событиями
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def init(self):
        pass

    def get_actions(self, _user_id):
        """
        Возвращает список действий, сделанных авторизованным пользователем(если авторизованный пользователь админ,
        то возвращает список действий всех пользователей, которые есть в системе)

        Returns:
            actions(List): список испытуемых
        """

        action_manager = ActionManager()

        return action_manager.get_actions(_user_id)

    '''
    def get_current_user(self):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)

        Return:
            User: пользователь
        """
        from services.user_manager_service import UserManagerService

        user_manager = UserManagerService()

        return user_manager.get_current_user('')
    '''

    def add_notifications(self, _place, _action, _action_place, _name_place, _login_user):
        """
        Процедура записи нового действия пользователя

        Args:
            _login_user (String): логин пользователя
            _name_place (String): название данных, где было совершенно действие
            _action (date, optional): действие пользователя
            _action_place(String): что именно изменил/добавил пользователь
            _place (String): тип места, где было совершенно действие
        """

        action_manager = ActionManager()

        return action_manager.add_notifications(_login_user, _name_place, _action, _action_place, _place)