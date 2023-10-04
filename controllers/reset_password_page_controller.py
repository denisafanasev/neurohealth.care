from typing import Union

from flask_mail import Mail

from error import UserManagerException, OneTimeLinkManagerException
from services.reset_password_service import ResetPasswordService


class ResetPasswordPageController:
    """
    
    """

    def send_link_for_email(self, _email: str, _mail: Mail) -> (str, str):
        """
        Передает почту пользователя для отправки одноразовой ссылки
        """
        reset_password_service = ResetPasswordService()

        try:
            reset_password_service.send_link_for_email(_email, _mail)

        except UserManagerException as error:

            return str(error), 'Error'

        return 'Сообщение для восстановления пароля была отправлена на вашу почту', 'Successful'

    def reset_password(self, _link: str, _password: str, _password2: str) -> (str, str):
        """
        Передает новый пароль пользователя
        """
        reset_password_service = ResetPasswordService()

        try:
            reset_password_service.reset_password(_link, _password, _password2)
        except OneTimeLinkManagerException as error:
            return str(error), 'Error'

        return 'Пароль успешно изменен!', 'Successful'
