class HomeworkChat():
    """
    Класс Чата
    """
    def __init__(self, _id=None, _id_user=None, _id_lesson=None, _unread_message_amount=0):
        """
        Конструктор класса

        Args:
            _id(Integer): ID комнаты чата. Defaults to None
            _id_user(Integer): ID пользователя. Defaults to None
            _id_lesson(Integer): ID урока. Defaults to None
            _unread_message_amount(Integer): количество непрочитанных сообщений в чате. Defaults to 0
        """
        self.id = _id
        self.id_user = _id_user
        self.id_lesson = _id_lesson
        self.message = None
        self.unread_message_amount = _unread_message_amount