class Message():
    """
    Класс Сообщение
    """
    def __init__(self, _id=None, _id_user=None, _text='', _date_send='', _id_homework_chat=None, _read=False):
        """
        Конструктор класса

        Args:
            _id(Int): ID сообщения. Defaults to None
            _text(String): текст сообщения. Defaults to ""
            _date_send(String): дата отправки сообщения. Defaults to ""
            _id_user(Int): ID пользователя. Defaults to None
            _id_homework_chat(Int): ID комнаты чата. Defaults to None
            _read(Boolean): просмотрено ли сообщение. Defaults to False
        """
        self.id = _id
        self.id_user = _id_user
        self.text = _text
        self.date_send = _date_send
        self.id_homework_chat = _id_homework_chat
        self.read = _read