from typing import Union

from flask import url_for, render_template
from flask_mail import Mail

from models.email_message_text_manager import EmailMessageTextManager
from models.one_time_link_manager import OneTimeLinkManager
from models.user import User
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
        email_message_text_manager = EmailMessageTextManager()

        user = user_manager.get_user_by_email(_email)
        if user is None:
            raise UserManagerException('Пользователь с такой почтой не найден. Проверьте свою почту.')

        link = one_time_link_manager.created_one_time_link(user.user_id, 'reset_password')
        email_message_text = email_message_text_manager.get_email_message_text('email_confirmation')

        confirm_url = url_for('multilingual.reset_password', _anchor=link, _external=True)
        html = render_template('email_message_form.html', confirm_url=confirm_url, text=email_message_text.text,
                               footer=email_message_text.footer)

        mail_adapter.send_email(_email, 'Восстановление пароля', html, _mail)

    def get_user(self, _link: str) -> Union[User, None]:
        """
        Возвращает пользователя

        Args:
            _link: одноразовая ссылка для сброса пароля
        """
        user_manager = UserManager()
        one_time_link_manager = OneTimeLinkManager()

        one_time_link = one_time_link_manager.get_one_time_link(_link)
        if one_time_link is not None:

            user = user_manager.get_user_by_id(one_time_link.user_id)

            return user

    def reset_password(self, _link: str, _password: str, _password2: str) -> None:
        """
        Проверяет наличие ссылки в базе данных и ее действительность. Если все в порядке, то меняет пользователю пароль

        Args:
            _link:
            _password:
            _password2:
        """
        user_manager = UserManager()
        one_time_link_manager = OneTimeLinkManager()

        one_time_link = one_time_link_manager.get_one_time_link(_link)
        if one_time_link is None:
            return

        user_manager.chenge_password(one_time_link.user_id, _password, _password2)
        one_time_link_manager.deactivate_link(one_time_link.id)

