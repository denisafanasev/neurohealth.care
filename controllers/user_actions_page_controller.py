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