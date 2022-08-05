class Module():
    """
    Класс модуль
    """

    def __init__(self, _id=0, _name='', _lessons=None, _id_course=None):
        """
        Конструктор класса

        Args:
            _id(Integer): id модуля
            _name(String): название модуля
            _lessons(List): список уроков данного модуля
        """

        self.id = _id
        self.id_course = _id_course
        self.name = _name
        self.lessons = _lessons