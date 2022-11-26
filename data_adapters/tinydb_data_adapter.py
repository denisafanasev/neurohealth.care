from tinydb import TinyDB, Query, where
import json
from tinydb.operations import delete, increment, add
import config

class TinyDBDataAdapter():
    """
    Класс предназначен для работы с системой хранения данных
    Возвращается структуры типа Dict, а хранит данные в том виде
    в котором это предполагает используемый адаптер

    для разных структур может использовать разные адаптеры

    поддерживаемые системы хранения: TinyDB
    """

    data_store = None

    def __init__(self, _table_name, tinydb_table_name="_default"):
        """
        Возвращается объект хранилища данных по указанному типу данных
        @params:
            _type    - Required  : тип данных (String)
        """
        self.data_store = TinyDB(config.DATA_FOLDER + _table_name + ".json", encoding='utf-8', ensure_ascii=False)
        self.data_store = self.data_store.table(tinydb_table_name)

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
    
    def insert_row(self, _data):
        """
        Добавить новую запись в хранилище

        Args:
            _data (Dict): структура данных для записи

        Returns:
            Int: id созданной записи
        """        

        result = self.data_store.insert(_data)

        return result

    '''
    def change_row(self, _data):

        """
        Обновить запись в хранилище

        Args:
            _data (Dict): структура данных для записи
        """

        self.data_store.update_multiple([(_data, where("login") == _data["login"])])
    '''

    def update_row(self, _data, _where):
        """
        Обновление данных

        Args:
            _data(Dict): структура данных для записи
            _where(Dict): переменная для поиска нужной записи
        """

        self.data_store.update(_data, where(_where) == _data[_where])
    
    def update_row_by_id(self, _data, _id):
        """
        Обновление данных по id

        Args:
            _data(Dict): структура данных для записи
            _id(Int): id записи
        """

        self.data_store.update(_data, doc_ids = [_id])

    def delete_key_in_row(self, _key, _where, _where_value):
        """
        Удаление ключа и значения из записи
        Args:
            _key(String): ключ, который нужно удалить
            _where(String): ключ для поиска нужной записи
            _where_value(String): значение ключа для поиска нужной записи
        """

        self.data_store.update(delete(_key), where(_where) == _where_value)

    def delete_row(self, _data_ids):
        """
        Удаление записи
        Args:
            _data_ids(List): список из id записей, которые нужно удалить
        """

        self.data_store.remove(doc_ids=_data_ids)
