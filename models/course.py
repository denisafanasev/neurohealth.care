
class Module():
    """
    Класс модуль
    """

    def __init__(self, _id=0, _name='', _lessons=None):
        """
        Конструктор класса

        Args:
            _id(Integer): id модуля
            _name(String): название модуля
            _lessons(List): список уроков данного модуля
        """

        self.id = _id
        self.name = _name
        self.lessons = _lessons

class Lesson():
    """
    Класс урок
    """

    def __init__(self, _id=0, _id_module=0, _name='', _materials=None, _link='', _text='', _task=''):
        """
        Конструктор класса

        Args:
            _id(Integer): id урока
            _id_module(Integer): id модуля
            _name(String): название урока
            _materials(List): список дополнительных материалов к уроку
            _link(String): ссылка на видео для урока
            _text(String): текст для урока
            _task(String): задание к уроку
        """

        self.id = _id
        self.id_module = _id_module
        self.name = _name
        if _materials is not None:
            self.materials = _materials
        else:
            self.materials = []
        self.link = _link
        self.text = _text
        self.task = _task

class CoursesList():
    """
    Класс список курсов
    """

    def __init__(self, _id=0, _name='', _description='', _image='', _type=''):
        """
        Коструктор класса

        Args:
            _id(Integer): id курса
            _name(String): название курса
            _image(String): ссылка на картинку курса
            _description(String): краткое описание курса
        """

        self.id = _id
        self.name = _name
        self.description = _description
        self.image = _image
        self.type = _type

# TODO: надо это в класс курса перенести
class Setting():
    """
    Класс настройки
    """

    def __init__(self, _image):
        """
        Конструктор класса

        Args:
            _image(String): ссылка на изображение
        """

        self.image = _image

class Course():
    """
    Класс курса
    """

    def __init__(self, _id, _name, _description, _type):
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