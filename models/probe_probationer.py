from datetime import datetime

class Probe():
    """
    Класс теста
    """

    def __init__(self, _name_probationer="", _probationer_id="", _date_of_birth="", _protocol_status="",
                 _probe_id="", _estimated_values_file="", _test=""):
        """
        Конструктор класса

        Args:
            _name_probationer(String): имя тестируемого
            _probationer_id(Int): id тестируемого
            _date_of_birth(date, optional): дата рождения тестируемого
            _protocol_status(String): статус протокола(черновик/окончательный)
            _probe_id(Int): id теста
            _estimated_values_file(String): название файла, из которого беруться значения для данного тестируемого
        """

        self.name_probationer = _name_probationer
        self.probationer_id = _probationer_id
        self.estimated_values_file = _estimated_values_file
        self.date_test = datetime.strftime(datetime.today(), "%d/%m/%y")
        self.date_protocol = datetime.strftime(datetime.today(), "%d/%m/%y")
        self.probe_id = _probe_id
        self.test = _test

        if _date_of_birth != "":
            self.age_probationer = ((datetime.today() - datetime.strptime(_date_of_birth, "%d/%m/%Y")) / 365.25).days

        if _protocol_status == "end":
            self.protocol_status = "окончательный"
        elif _protocol_status == "draft":
            self.protocol_status = "черновик"
        elif _protocol_status == "черновик":
            self.protocol_status = "draft"
        elif _protocol_status == "окончательный":
            self.protocol_status = "end"
        else:
            self.protocol_status = "черновик"