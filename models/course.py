class Course():
    """
    Класс Курс
    """

    def __init__(self, _id=None, _name='', _description='', _type='', _image=None):
        """
        Конструктор класса

        Args:
            _id(Integer): id курса
            _name(String): имя курса
            _description(String): описание курса
            _type(String): тип курса
        """

        self.id = _id
        self.name = _name
        self.description = _description
        self.type = _type
        self.image = _image