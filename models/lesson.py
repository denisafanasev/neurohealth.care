class Lesson():
    """
    Класс урок
    """

    def __init__(self, _id=None, _id_module=None, _name='', _materials=None, _link='', _text='', _task=''):
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
