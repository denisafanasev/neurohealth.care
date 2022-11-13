class Module():
    """
    Класс модуль
    """

    def __init__(self, _id=None, _name='', _lessons=None, _id_course=None):
        """
        Конструктор класса

        Args:
            _id(Integer): ID модуля. Defaults to None
            _name(String): название модуля. Defaults to ""
            _lessons(List): список уроков данного модуля. Defaults to None
            _id_course(Integer): ID курса. Defaults to None
        """

        self.id = _id
        self.id_course = _id_course
        self.name = _name
        self.lessons = _lessons