from data_adapters.data_store import DataStore
from models.email_message_text import EmailMessageText


class EmailMessageTextManager:

    def email_message_text_row_to_email_message_text(self, _data_row: dict) -> EmailMessageText:
        """

        """
        email_message_text = EmailMessageText(_id=_data_row['id'], _name=_data_row['name'], _text=_data_row['text'],
                                              _footer=_data_row['footer'])

        return email_message_text

    def get_email_message_text(self, _name: str) -> EmailMessageText:
        """

        """
        data_store = DataStore('email_message_text')

        email_message_text_data = data_store.get_rows({'name': _name})
        if email_message_text_data:
            return self.email_message_text_row_to_email_message_text(email_message_text_data[0])