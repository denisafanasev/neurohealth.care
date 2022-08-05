from data_adapters.data_store import DataStore
from models.module import Module


class ModuleManager():
    """
    Класс модели управления модулями курсов
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """
    def module_row_to_module(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о уроке в структуру Course

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Module: курс
        """

        module = Module(_data_row.doc_id, _data_row["name"], _data_row["lessons"])

        return module

    def get_course_modules_list(self, _id=1):
        """
        Возвращает список модулей курса по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            modules_list(List): списко модулей курса
        """

        data_store_module = DataStore("modules")

        modules = data_store_module.get_rows()
        modules_list = []
        for module in modules:
            modules_list.append(self.module_row_to_module(module))

        return modules_list