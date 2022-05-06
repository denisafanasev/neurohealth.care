class Estimated_Values():
    """
    Класс оценочные значения
    """

    def __init__(self, _id, _assessment_parameters, _tests):
        """
        Конструктор класса

        Args:
            _id(Integer): id пробы
            _assessment_parameters(String): название пробы
            _tests(List): список тестов данной пробы
        """

        self.assessment_parameters = _assessment_parameters
        self.tests = _tests
        self.id = _id
