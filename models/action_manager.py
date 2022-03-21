from data_adapters.data_store import DataStore
from models.action import Action


class ActionManager():

    def action_row_to_action(self, _user_login, _action):
        """
        Преобразует структуру данных, в которой хранится информация о действиях пользователя в структуру Action
        Args:
            _user_login (String): логин пользователя
            _action (List): список действий пользователя
        """

        action = Action(_user_login, _action)

        return action

    def add_notifications(self, _user, _name_place, _action, _place):
        """
        Процедура записи нового действия пользователя

        Args:
            _user (String): логин пользователя
            _name_place (String): название данных, где было совершенно действие
            _action (date, optional): действие пользователя
            _place (String): тип места, где было совершенно действие
        """

        data_store = DataStore("action")


        if _action == "overwrite":
            _action = "изменил"
        elif _action == "add":
            _action = "добавил"

        if _name_place == "estimated_values":
            _name_place = "в файле"
        elif _name_place == "probationer_manager":
            _name_place = "испытуемого"
        elif _name_place == "user_manager":
            _name_place = "пользователя"

        action = "{user} {action} данные {place} {name_place}".format(
            user=_user,
            place=_place,
            action=_action,
            name_place=_name_place)

        action = self.action_row_to_action(_user, action)

        if not self.is_there_users_action(action.user_login):
            data_store.add_row({"login": action.user_login, "action": [action.action]})
        else:
            data_store.update_action(action.action, action.user_login)

    def get_actions(self):
        """
        Возвращает список действий, сделанных авторизованным пользователем(если авторизованный пользователь админ,
        то возвращает список действий всех пользователей, которые есть в системе)

        Returns:
            actions(List): список испытуемых
        """

        data_store = DataStore("action")
        from models.user_manager import UserManager

        actions_list = data_store.get_rows()
        user = UserManager().get_user_by_id(UserManager().get_current_user_id())
        actions = []

        for i_action in actions_list:
            if not user.role == "superuser":
                if user.login == i_action["login"]:
                    action = self.action_row_to_action(i_action["login"], i_action["action"])
                    actions.extend(action.action)
            else:
                action = self.action_row_to_action(i_action["login"], i_action["action"])
                actions.append(action)

        return actions

    def is_there_users_action(self, _login):
        """
        Проверяет, записаны ли действия авторизованного пользователя
        """

        data_store = DataStore("action")
        users_action = data_store.get_rows({"login": _login})

        if users_action != []:
            return True
        else:
            return False