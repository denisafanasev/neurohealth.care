class Message():
    """
    Класс Сообщение
    """
    def __init__(self, _id=0, _id_user='', _text='', _date_send='', _id_room_chat=None, _read=False):
        """
        Конструктор класса

        Args:
            _id(Int): ID сообщения
            _text(String): текст сообщения
            _date_send(String): дата отправки сообщения
            _id_user(Int): ID пользователя
            _id_room_chat(Int): ID комнаты чата
            _read(Boolean): просмотрено ли сообщение
        """
        self.id = _id
        self.id_user = _id_user
        self.text = _text
        self.date_send = _date_send
        self.id_room_chat = _id_room_chat
        self.read = _read