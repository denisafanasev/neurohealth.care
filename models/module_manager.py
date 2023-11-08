from data_adapters.data_store import DataStore
from models.module import Module


class EducationModuleManager():
    """
    Класс модели управления модулями курсов
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """
    def module_row_to_module(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация об модуле курса в структуру Module

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Module: модуль курса
        """

        doc_id = _data_row['doc_id'] if _data_row.get('doc_id') is not None else _data_row.doc_id
        module = Module(_id=doc_id, _name=_data_row["name"], _id_course=_data_row['id_course'])

        if _data_row.get("lessons") is not None:
            module.lessons = _data_row['lessons']

        return module

    def get_course_modules_list(self, _id=1):
        """
        Возвращает список модулей курса по id

        Args:
            _id(Int): ID курса. Defaults to 1

        Returns:
            modules_list(List): список модулей курса
        """

        data_store_module = DataStore("modules")

        modules = data_store_module.get_rows({"id_course": _id})
        if modules:
            modules_list = []
            for module in modules:
                modules_list.append(self.module_row_to_module(module))

            return modules_list

    def get_module_by_id(self, _id):
        """
        Возвращает модуль по ID

        Args:
            _id(Int): ID модуля

        Return:
            Module: модуль
        """

        data_store = DataStore("modules")

        module = data_store.get_row_by_id(_id)
        if module is not None:
            module = self.module_row_to_module(module)

        return module

    def get_count_modules_by_id_course(self, _id_course: list) -> int:
        """
        Возвращает количество модулей курса по ID курсу

        Args:
            _id_course: ID курса

        Returns:
            список ID модулей
        """
        data_store = DataStore('modules', force_adapter='PostgreSQLDataAdapter')

        data = data_store.get_rows_count({'where': f'id_course = {_id_course}'})

        return data
