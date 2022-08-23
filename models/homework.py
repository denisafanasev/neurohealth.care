
class Homework():
    """
    Класс Домашняя работа
    """
    def __init__(self, _id=None, _users_files_list=None, _text=None, _id_user=None, _id_lesson=None, _status=None,
                 _date_delivery=None):
        """
        Конструктор класса

        Args:
            _id(Integer): ID домашней работы
            _users_files_list(List): список уникальных имен файлов домашне работы
            _text(String): текст домашней работы
            _id_user(Integer): ID пользователя
            _id_lesson(Integer): ID урока
            _status(Boolean): Принята/Не принята домашняя работа
            _date_delivery(String): дата сдачи домашней работы
        """

        self.id = _id
        self.id_user = _id_user
        self.id_lesson = _id_lesson
        self.users_files_list = _users_files_list
        self.text = _text
        self.status = _status
        self.date_delivery = _date_delivery