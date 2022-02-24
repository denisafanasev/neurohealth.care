class Action():

    def __init__(self, _user_name="", _user_login="", _place="", _action="", _name_place=""):

        self.user_login = _user_login

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


        self.action = "Пользователь {user} {action} данные {name_place} {place}".format(
            user=_user_name,
            place=_place,
            action=_action,
            name_place=_name_place)