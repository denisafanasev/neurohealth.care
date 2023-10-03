from jinja2 import Markup


class EmailMessageText:
    """
    Текст сообщения, которое отправляют пользователю по почте
    """
    def __init__(self, _id: int = 0, _name: str = '', _text: str = '', _footer: str = ''):
        """

        """
        self.id = _id
        self.name = _name
        self.text = Markup(_text)
        self.footer = Markup(_footer)
