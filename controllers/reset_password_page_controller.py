from typing import Union

from flask_mail import Mail

from error import UserManagerException
from services.reset_password_service import ResetPasswordService


class ResetPasswordPageController:
    """
    
    """

    def send_link_for_email(self, _email: str, _mail: Mail) -> str:
        """

        """
        reset_password_service = ResetPasswordService()

        try:
            reset_password_service.send_link_for_email(_email, _mail)

        except UserManagerException as error:

            return str(error)

        return 'Сообщение для восстановления пароля была отправлена на вашу почту'

    def reset_password(self, _link: str, _password: str, _password2: str) -> str:
        """

        """
        reset_password_service = ResetPasswordService()

        reset_password_service.reset_password(_link, _password, _password2)

        return 'Пароль успешно изменен!'

    def get_user_name(self, _link: str) -> dict:
        """
        Возвращает имя пользователе

        Args:
            _link: одноразовая ссылка для сброса пароля

        Returns:
            user_name
        """
        reset_password_service = ResetPasswordService()

        user = reset_password_service.get_user(_link)

        if user is not None:
            return user.name
