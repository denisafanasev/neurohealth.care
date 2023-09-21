from models.user_manager import UserManager


class EmailConfirmationService():

    def email_confirmation(self, _token):
        """

        """
        user_manager = UserManager()

        user = user_manager.get_user_by_token(_token)
        if user is not None:
            user_manager.email_confirmation(user.user_id)


            return user

        return False
