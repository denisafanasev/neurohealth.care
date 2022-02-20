from tinydb import TinyDB, Query, where
import json
from tinydb.operations import delete, increment

class DataStore():
    """
    Класс предназначен для работы с системой хранения данных
    Возвращается структуры типа Dict, а хранит данные в том виде
    в котором это предполагает используемый адаптер

    для разных структур может использовать разные адаптеры

    поддерживаемые системы хранения: TinyDB
    """

    data_store = None

    def __init__(self, _type, _table="_default"):
        """
        Возвращается объект хранилища данных по указанному типу данных
        @params:
            _type    - Required  : тип данных (String)
        """
        self.data_store = TinyDB("data/" + _type + ".json")

        if _table != "_default":
            self.data_store = self.data_store.table(_table)

    def get_rows(self, _filter=None):
        """
        Возвращается записи, которые соответствуют заданному критерию из заданной таблицы в виде списка Dict

        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        result = []

        if _filter is not None:
            result = self.data_store.search(Query().fragment(_filter))
        else:
            result = self.data_store.all()

        return result

    def get_row_by_id(self, _id):
        """
        Возвращается записи, которые соответствуют заданному критерию из заданной таблицы в виде списка Dict

        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        result = None

        if _id != '':
            result = self.data_store.get(doc_id=int(_id))

        return result

    def get_rows_count(self, _filter=""):
        """
        Возвращается количество записей, которые соответствуют заданному критерию из заданной таблицы
        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        result = 0

        result = len(self.get_rows(_filter))

        return result
    
    def add_row(self, _data):
        """
        Добавить новую запись в хранилище

        Args:
            _data (Dict): структура данных для записи

        Returns:
            Int: id созданной записи
        """        

        result = self.data_store.insert(_data)

        return result

    def change_row(self, _data):

        """
        Обновить запись в хранилище

        Args:
            _data (Dict): структура данных для записи
        """

        self.data_store.update_multiple([({"name": _data["name"], "email":_data["email"], "role":_data["role"],
                                           "probationers_number":_data["probationers_number"],
                                           "expires_date":_data["expires_date"], "access_time":_data["access_time"],
                                           "active":_data["active"]}, where("login") == _data["login"])])

    def discharge_password(self, _data):
        """
        Сброс пароля

        Args:
            _data (Dict): структура данных для записи
        """

        self.data_store.update({"password": _data["password"]}, where("login") == _data["login"])

    def update_row(self, _data, _where):

        self.data_store.update(_data, where(_where) == _data[_where])

    def change_probationer(self, _data):

        self.data_store.update_multiple([({"name_probationer": _data["name_probationer"],
                                           "date_of_birth": _data["date_of_birth"], "name_parent": _data["name_parent"],
                                           "educational_institution": _data["educational_institution"],
                                           "contacts": _data["contacts"],"diagnoses": _data["diagnoses"],
                                           "reasons_for_contact": _data["reasons_for_contact"]},
                                           where("probationer_id") == _data["probationer_id"])])

    # def increment_key_row(self, _key, _where):
    #
    #     self.data_store.update(increment(_key))