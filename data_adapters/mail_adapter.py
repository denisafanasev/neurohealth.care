from flask import Flask
from flask_mail import Message, Mail

import config

class MailAdapter():

    def send_email(to, subject, template):
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=config.MAIL_DEFAULT_SENDER
        )

        app = Flask(__name__)
        mail = Mail(app)

        mail.send(msg)
