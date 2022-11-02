from tinydb import TinyDB, Query, where
import json
from tinydb.operations import delete, increment, add

from data_adapters.tinydb_data_adapter import TinyDBDataAdapter
from data_adapters.postgresql_data_adapter import PostgreSQLDataAdapter

import config

class DataStore():
    """
    Класс предназначен для работы с системой хранения данных
    Возвращается структуры типа Dict
    
    The type of the adapter is defined in depends on the system configuration
    Currently the following adapters are supported: TinyDB, PostgreSQL
    """

    data_store = None

    def __init__(self, _table_name, tinydb_table_name="_default", force_adapter=None):
        """
        Возвращается объект хранилища данных по указанному типу данных
        @params:
            _table_name    - Required  : имя структуры/таблицы хранения данных (String)
            _force_adapter - Optional  : имя дата адаптера, если нужно использовать отличный от того, который указан в настройках системы
        """

        if force_adapter is None:
            force_adapter = config.data_adapter()

        if force_adapter == "PostgreSQLDataAdapter":
            self.data_store = PostgreSQLDataAdapter(_table_name)

        elif force_adapter == "TinyDBDataAdapter":
            self.data_store = TinyDBDataAdapter(_table_name, tinydb_table_name)

        else:
            raise Exception("Unknown adapter")

    def get_rows(self, _filter=None):
        """
        Возвращается записи, которые соответствуют заданному критерию из заданной таблицы в виде списка Dict

        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        result = []

        result = self.data_store.get_rows(_filter)

        return result

    def get_row_by_id(self, _id):
        """
        Возвращается записи, которые соответствуют заданному критерию из заданной таблицы в виде списка Dict

        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        result = None

        result = self.data_store.get_row_by_id(_id)

        return result

    def get_rows_count(self, _filter=""):
        """
        Возвращается количество записей, которые соответствуют заданному критерию из заданной таблицы
        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        result = 0

        result = self.data_store.get_rows_count(_filter)

        return result
    
    def insert_row(self, _data):
        """
        Добавить новую запись в хранилище

        Args:
            _data (Dict): структура данных для записи

        Returns:
            Int: id созданной записи
        """

        result = self.data_store.insert_row(_data)

        return result

    def update_row(self, _data, _where):
        """
        Обновление данных

        Args:
            _data(Dict): структура данных для записи
            _where(Dict): переменная для поиска нужной записи
        """

        self.data_store.update_row(_data, _where)
    
    def update_row_by_id(self, _data, _id):
        """
        Обновление данных по id

        Args:
            _data(Dict): структура данных для записи
            _id(Int): id записи
        """

        self.data_store.update_row_by_id(_data, _id)

    # TODO: убрать отсюда этот метод
    def update_messages(self, _message, _id):
        """
        Обновление записей действий пользователей
        Args:
            _message(Dict): структура данных для записи
            _id(Int): переменная для поиска нужно записи
        """

        _data_store = None
        _data_store = TinyDB(config.DATA_FOLDER + "room_chat" + ".json", encoding='utf-8', ensure_ascii=False)
        _data_store.update(add("message", [_message]), where("id") == _id)

    # TODO: убрать отсюда этот метод
    def chenge_password(self, _data):
        """
        Сброс пароля

        Args:
            _data (Dict): структура данных для записи
        """

        _data_store = None
        _data_store = TinyDB(config.DATA_FOLDER + "users" + ".json", encoding='utf-8', ensure_ascii=False)
        _data_store.update({"password": _data["password"]}, where("login") == _data["login"])
    
    # TODO: убрать отсюда этот метод
    def change_probationer(self, _data):
        """
        Обновление данных тестируемого

        Args:
            _data(Dict): структура данных для записи
        """

        _data_store = None
        _data_store = TinyDB(config.DATA_FOLDER + "users" + ".json", encoding='utf-8', ensure_ascii=False)
        _data_store.update_multiple([(_data, where("probationer_id") == int(_data["probationer_id"]))])