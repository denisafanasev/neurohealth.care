from services.email_confirmation_service import EmailConfirmationService


class EmailConfirmationPageController():

    def email_confirmation(self, _token):

        email_confirmation_service = EmailConfirmationService()

        user = email_confirmation_service.email_confirmation(_token)

        if user is not None:
            error_message = 'Почто успешно подтверждена! Вы можете войти в систему!'
            status_code = 'Success'

        else:
            error_message = 'Не удалось подтвердить почту. Попробуйте позднее повторить попытку.'
            status_code = 'Error'

        return user, error_message, status_code
