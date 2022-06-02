from data_adapters.data_store import DataStore
from models.action import Action
from datetime import datetime, timedelta


class ActionManager():

    def action_row_to_action(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о действиях пользователя в структуру Action
        Args:
            _user_login (String): логин пользователя
            _action (List): список действий пользователя
        """

        action = Action(_data_row['id'], _data_row["login"], _data_row["action"])

        if _data_row.get("created_date") is not None:
            action.created_date = datetime.strptime(_data_row["created_date"], '%d/%m/%Y %H:%M:%S')
        else:
            action.created_date = datetime.now()

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
        elif _action == "view":
            _action = "посмотрел"

        if _name_place == "estimated_values":
            _name_place = "в файле"
            _place = "данные " + str(_place)
        elif _name_place == "probationer_manager":
            _name_place = "испытуемого"
            _place = "данные " + str(_place)
        elif _name_place == "user_manager":
            _name_place = "пользователя"
            _place = "данные " + str(_place)
        elif _name_place == "probes_manager":
            _name_place = ""
            _place = "данные " + str(_place)
        elif _name_place == "course_manager":
            _name_place = ""
            _place = f"урок {_place.lessons.name} модуля {_place.lessons.id_module}"

        action = "{user} {action} {place} {name_place}".format(
            user=_user,
            place=_place,
            action=_action,
            name_place=_name_place)
        id = data_store.get_rows_count() + 1
        action = self.action_row_to_action({"id": id, "login": _user, "action": action})

        data_store.add_row({"id": action.id, "login": action.user_login, "action": action.action,
                            "created_date": action.created_date.strftime("%d/%m/%Y %H:%M:%S")})

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

        date = datetime.now()
        actions = []

        for i_action in actions_list:
            if not user.role == "superuser":
                if user.login == i_action["login"]:
                    action = self.action_row_to_action(i_action)
                    if date < action.created_date:
                        actions.append({"action": action, "timedelta": date - date})
                        data_store.update_row({"created_date": date.strftime("%d/%m/%Y %H:%M:%S"), "id": action.id}, "id")
                    else:
                        actions.append({"action": action, "timedelta": date - action.created_date})
                    # timedelta_list.append(date - action.created_date)
            else:
                action = self.action_row_to_action(i_action)
                if date < action.created_date:
                    actions.append({"action": action, "timedelta": date - date})
                    data_store.update_row({"created_date": date.strftime("%d/%m/%Y %H:%M:%S"), "id": action.id}, "id")
                else:
                    actions.append({"action": action, "timedelta": date - action.created_date})
                # timedelta_list.append(date - action.created_date)

        # timedelta_list.sort()
        actions_list = sorted(actions, key=lambda d: d["timedelta"])
        actions = []

        if len(actions_list) >= 10:
            amount = 10
        else:
            amount = len(actions_list)

        for i_action in range(amount):
            time_ago = actions_list[i_action]['timedelta']
            hours = time_ago.seconds // 3600
            minutes = (time_ago.seconds % 3600) // 60
            seconds = (time_ago.seconds % 60)
            if time_ago.days == 0:
                if hours == 0:
                    if minutes == 0:
                        if seconds == 0:
                            actions_list[i_action]['timedelta'] = "только что"
                        else:
                            actions_list[i_action]['timedelta'] = f"{seconds} секунд назад"
                    elif minutes > 0:
                        actions_list[i_action]['timedelta'] = f"{minutes} минут назад"
                elif hours > 0:
                    actions_list[i_action]['timedelta'] = f"{hours} часов назад"
            elif time_ago.days > 0:
                if time_ago.days >= 7:
                    if time_ago.days < 28:
                        actions_list[i_action]['timedelta'] = f"{time_ago.days // 7} недель назад"
                    else:
                        actions_list[i_action]['timedelta'] = f"{actions_list[i_action]['action'].created_date.strftime('%d/%m/%Y')}"
                else:
                    actions_list[i_action]['timedelta'] = f"{time_ago.days} дней назад"

            actions.append(actions_list[i_action])



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