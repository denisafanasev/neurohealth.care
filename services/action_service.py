from models.action_manager import ActionManager
class ActionService():
    """
    EstimatedValuesService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def init(self):
        pass

    def get_actions(self):
        """
        Возвращает список действий, сделанных авторизованным пользователем(если авторизованный пользователь админ,
        то возвращает список действий всех пользователей, которые есть в системе)

        Returns:
            actions(List): список испытуемых
        """

        action_manager = ActionManager()

        return action_manager.get_actions()

    def get_current_user(self):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)

        Return:
            User: пользователь
        """
        
        # TODO: жесть какаято, надо переделать
        from models.user_manager import UserManager
        user_manager = UserManager()

        return user_manager.get_user_by_id(user_manager.get_current_user_id())

    def add_notifications(self, _place, _action, _name_place):
        """
        Процедура записи нового действия пользователя

        Args:
            _name_place (String): название данных, где было совершенно действие
            _action (date, optional): действие пользователя
            _place (String): тип места, где было совершенно действие
        """

        action_manager = ActionManager()

        user = self.get_current_user().login

        return action_manager.add_notifications(user, _name_place, _action, _place)