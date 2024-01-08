from models.action_manager import ActionManager
from models.user_manager import UserManager


class UserActionsService():

    def get_actions_by_user_id(self, _user_id):
        """
        Возвращает список действий, совершенных пользователем

        Args:
            _user_id(Int): ID

        Returns:
            List(Action): список действий
        """
        action_manager = ActionManager()
        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)
        if user is not None:
            return action_manager.get_actions_by_user(user)