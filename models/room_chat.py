class RoomChat():
    """
    Класс Комната Чата
    """
    def __init__(self, _id=None, _id_education_stream=None, _id_user=None, _id_lesson=None):
        """
        Конструктор класса

        Args:
            _id(Int): ID комнаты чата
            _id_user(Int): ID пользователя
            _id_lesson(Int): ID урока
            # _id_education_stream(Int): ID обучающего потока
        """
        self.id = _id
        # self.id_education_stream = _id_education_stream
        self.id_user = _id_user
        self.id_lesson = _id_lesson