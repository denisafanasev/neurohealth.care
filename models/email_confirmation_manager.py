from data_adapters.mail_adapter import MailAdapter

class EmailConfirmationManager():

    def __init__(self):
        self.mail_adapter = MailAdapter()

    def send_email(self, to, subject, template, mail):
        self.mail_adapter.send_email(to, subject, template, mail)