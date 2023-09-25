from flask import Flask
from flask_mail import Message, Mail

import config

class MailAdapter():

    def send_email(self, to, subject, template, mail):
        data_mail = config.data_mail()
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=data_mail['MAIL_USERNAME']
        )

        # app = Flask(__name__)
        # mail = Mail(app)

        mail.send(msg)
