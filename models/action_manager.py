from data_adapters.data_store import DataStore
from models.action import Action


class ActionManager():

    def action_row_to_action(self, _user_name, _user_login, _place, _action, _name_place):

        action = Action(_user_name, _user_login, _place, _action, _name_place)

        return action

    def add_notifications(self, _place, _action, _name_place):

        data = DataStore("action")
        from models.user_manager import UserManager

        user = UserManager().get_user_by_id(UserManager().get_current_user_id())
        action = self.action_row_to_action(user.name, user.login, _place, _action, _name_place)

        data.add_row({"login": action.user_login, "action": action.action})