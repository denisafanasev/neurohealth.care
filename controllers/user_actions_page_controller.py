import config
from services.user_actions_service import UserActionsService


class UserActionsPageController():

    def get_actions(self, _user_id):
        """
        Возвращает список действий, сделанных пользователем

        Args:
            _user_id(Int): ID

        Returns:
            actions_list_view(List): список действий
        """

        user_actions_service = UserActionsService()

        actions_list = user_actions_service.get_actions_by_user_id(_user_id)

        actions_list_view = []
        for action in actions_list:
            action_view = {
                'id': action.id,
                'action': action.action,
                'comment_action': action.comment_action,
                'created_date': action.created_date.strftime('%d/%m/%Y')
            }

            actions_list_view.append(action_view)

        return actions_list_view

    def get_menu_user_profile(self):
        """
        Возвращает список меню на странице "Профиль пользователя"
        """
        user_profile_menu = []
        for item in config.USER_PROFILE_MENU:
            if item['endpoint'] == 'user_actions':
                item['is_active'] = True
            else:
                item['is_active'] = False

            user_profile_menu.append(item)

        return user_profile_menu