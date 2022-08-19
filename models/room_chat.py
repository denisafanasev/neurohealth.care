class RoomChat():
    """
    Класс Комната Чата
    """
    def __init__(self, _id=None, _id_education_stream=None, _id_user=None, _id_lesson=None, _unread_message_amount=0):
        """
        Конструктор класса

        Args:
            _id(Integer): ID комнаты чата
            _id_user(Integer): ID пользователя
            _id_lesson(Integer): ID урока
            # _id_education_stream(Integer): ID обучающего потока
            _unread_message_amount(Integer): количество непрочитанных сообщений в чате
        """
        self.id = _id
        # self.id_education_stream = _id_education_stream
        self.id_user = _id_user
        self.id_lesson = _id_lesson
        self.message = None
        self.unread_message_amount = _unread_message_amount