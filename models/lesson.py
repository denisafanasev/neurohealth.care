class Lesson():
    """
    Класс урок
    """

    def __init__(self, _id=None, _id_module=None, _name='', _materials=None, _link='', _text=None, _task=None):
        """
        Конструктор класса

        Args:
            _id(Integer): id урока. Defaults to None
            _id_module(Integer): id модуля. Defaults to None
            _name(String): название урока. Defaults to ""
            _materials(List): список дополнительных материалов к уроку. Defaults to None
            _link(String): ссылка на видео для урока. Defaults to ""
            _text(String): текст для урока. Defaults to None
            _task(String): задание к уроку. Defaults to None
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
