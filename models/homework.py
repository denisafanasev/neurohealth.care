
class Homework():
    """
    Класс Домашняя работа
    """
    def __init__(self, _id=None, _users_files_list=None, _text=None, _id_user=None, _id_lesson=None, _status=None,
                 _date_delivery=None):
        """
        Конструктор класса

        Args:
            _id(Integer): ID домашней работы. Defaults to None
            _users_files_list(List): список уникальных имен файлов домашне работы. Defaults to None
            _text(String): текст домашней работы. Defaults to None
            _id_user(Integer): ID пользователя. Defaults to None
            _id_lesson(Integer): ID урока. Defaults to None
            _status(Boolean): Принята/Не принята домашняя работа. Defaults to None
            _date_delivery(String): дата сдачи домашней работы. Defaults to None
        """

        self.id = _id
        self.id_user = _id_user
        self.id_lesson = _id_lesson
        self.users_files_list = _users_files_list
        self.text = _text
        self.status = _status
        self.date_delivery = _date_delivery