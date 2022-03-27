from models.action_manager import ActionManager


class ActionService():

    def init(self):
        pass

    def get_actions(self):

        action_manager = ActionManager()

        return action_manager.get_actions()

    def get_current_user(self):

        from models.user_manager import UserManager
        user_manager = UserManager()

        return user_manager.get_user_by_id(user_manager.get_current_user_id())

    def add_notifications(self, _place, _action, _name_place):

        action_manager = ActionManager()

        user = self.get_current_user().login

        return action_manager.add_notifications(user, _place, _action, _name_place)