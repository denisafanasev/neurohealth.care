from sqlalchemy import create_engine
import config

class PostgreSQLDataAdapter():
    """
    Класс предназначен для работы с системой хранения данных
    Возвращается структуры типа Dict, а хранит данные в том виде
    в котором это предполагает используемый адаптер

    для разных структур может использовать разные адаптеры

    поддерживаемые системы хранения: PostgreSQL
    """

    data_store = None
    table_name = None

    def __init__(self, _table_name):
        """
        Возвращается объект хранилища данных по указанному типу данных
        @params:
            _table_name    - Required  : имя таблицы данных (String)
        """

        self.table_name = _table_name
        self.data_store = create_engine("postgresql+psycopg2:" + config.PostgreSQLDataAdapter_connection_string())

    def get_rows(self, _filter=None):
        """
        Возвращается записи, которые соответствуют заданному критерию из заданной таблицы в виде списка Dict

        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        result = []

        #if _filter is not None:
        #    result = self.data_store.search(Query().fragment(_filter))
        #else:
        #    result = self.data_store.all()

        return result

    def get_row_by_id(self, _id):
        """
        Возвращается записи, которые соответствуют заданному критерию из заданной таблицы в виде списка Dict

        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        result = None

        #if _id != '':
        #    result = self.data_store.get(doc_id=int(_id))

        return result

    def get_rows_count(self, _filter=""):
        """
        Возвращается количество записей, которые соответствуют заданному критерию из заданной таблицы
        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        result = 0

        # result = len(self.get_rows(_filter))

        return result
    
    def add_row(self, _data):
        """
        Добавить новую запись в хранилище

        Args:
            _data (Dict): структура данных для записи

        Returns:
            Int: id созданной записи
        """        

        result = None

        # result = self.data_store.insert(_data)

        return result

    def change_row(self, _data):

        """
        Обновить запись в хранилище

        Args:
            _data (Dict): структура данных для записи
        """

        # self.data_store.update_multiple([(_data, where("login") == _data["login"])])

    def update_row(self, _data, _where):
        """
        Обновление данных

        Args:
            _data(Dict): структура данных для записи
            _where(Dict): переменная для поиска нужной записи
        """

        # self.data_store.update(_data, where(_where) == _data[_where])
    
    def update_row_by_id(self, _data, _id):
        """
        Обновление данных по id

        Args:
            _data(Dict): структура данных для записи
            _id(Int): id записи
        """

        # self.data_store.update(_data, doc_ids = [_id])


    def upsert_row(self, _data, _where):
        """
        Обновление данных

        Args:
            _data(Dict): структура данных для записи
            _where(Dict): переменная для поиска нужно записи
        """

        # self.data_store.upsert(_data, where(_where) == _data[_where])

    def delete_key_in_row(self, _key, _where, _where_value):
        """
        Удаление ключа и значения из записи
        Args:
            _key(String): ключ, который нужно удалить
            _where(String): ключ для поиска нужной записи
            _where_value(String): значение ключа для поиска нужной записи
        """

        # self.data_store.update(delete(_key), where(_where) == _where_value)
    