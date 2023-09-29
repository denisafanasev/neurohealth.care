from typing import Union

from flask import url_for, render_template
from flask_mail import Mail

from models.one_time_link_manager import OneTimeLinkManager
from models.user_manager import UserManager
from data_adapters.mail_adapter import MailAdapter
from error import UserManagerException


class ResetPasswordService:
    """

    """
    def send_link_for_email(self, _email: str, _mail: Mail) -> None:
        """
        Создает ссылку для смены пароля и отправляет пользователю на почту
        """
        user_manager = UserManager()
        one_time_link_manager = OneTimeLinkManager()
        mail_adapter = MailAdapter()

        user = user_manager.get_user_by_email(_email)
        if user is None:
            raise UserManagerException('Пользователь с такой почтой не найден. Проверьте свою почту.')

        link = one_time_link_manager.created_one_time_link(user.user_id, 'reset_password')

        confirm_url = url_for('multilingual.reset_password', _anchor=link, _external=True)
        print(confirm_url)
        html = render_template('reset_password_message.html', confirm_url=confirm_url)

        mail_adapter.send_email(_email, 'Сброс пароля', html, _mail)

