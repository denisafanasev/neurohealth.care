from typing import Union

from flask_mail import Mail

from error import UserManagerException
from services.reset_password_service import ResetPasswordService


class ResetPasswordPageController:
    """
    
    """
    def send_link_for_email(self, _email: str, _mail: Mail) -> Union[None, str]:
        """

        """
        reset_password_service = ResetPasswordService()

        try:
            reset_password_service.send_link_for_email(_email, _mail)

        except UserManagerException as error:

            return str(error)