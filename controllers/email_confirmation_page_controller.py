from services.email_confirmation_service import EmailConfirmationService


class EmailConfirmationPageController():

    def email_confirmation(self, _token):
        """

        """
        email_confirmation_service = EmailConfirmationService()

        user = None
        if _token is not None:
            user = email_confirmation_service.email_confirmation(_token)

        if user is not None:
            error_message = 'Почта успешно подтверждена! Вы можете войти в систему!'
            is_email_confirmed = user.email_confirmed

        else:
            error_message = 'Не удалось подтвердить почту. Попробуйте позднее повторить попытку.'
            is_email_confirmed = False

        return user, error_message, is_email_confirmed
