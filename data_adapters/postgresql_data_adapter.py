import sqlalchemy as db
from sqlalchemy import create_engine, text
from sqlalchemy import insert, select, update
from sqlalchemy import MetaData

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
        self.data_store = create_engine("postgresql:" + config.PostgreSQLDataAdapter_connection_string())

    def get_rows(self, _filter=None):
        """
        Возвращается записи, которые соответствуют заданному критерию из заданной таблицы в виде списка Dict

        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        metadata = MetaData(bind=self.data_store)
        metadata.reflect()

        # query = select(metadata.tables[self.table_name])
        # if _filter is not None:
        #     query = query.where(text(_filter))

        if _filter is not None:
            query_result = self.data_store.execute(text(_filter))
        else:
            query_result = self.data_store.execute(select(metadata.tables[self.table_name]))

        result = [u._asdict() for u in query_result]

        return result

    def get_row_by_id(self, _id):
        """
        Возвращается записи, которые соответствуют заданному критерию из заданной таблицы в виде списка Dict

        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        result = None

        if _id != '':

            # read DB metadata
            metadata = MetaData(bind=self.data_store)
            metadata.reflect()

            # run select by doc_id (default primary key for each table)
            query_result = self.data_store.execute(
                select(metadata.tables[self.table_name]).where(metadata.tables[self.table_name].columns["doc_id"] == _id)
            )

            # convert sqlalchemy query result to list of dict
            result = [u._asdict() for u in query_result.all()]

        return result

    def get_rows_count(self, _filter=""):
        """
        Возвращается количество записей, которые соответствуют заданному критерию из заданной таблицы
        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """

        result = 0

        # read DB metadata
        metadata = MetaData(bind=self.data_store)
        metadata.reflect()

        query_result = db.select([db.func.count()]).select_from(metadata.tables[self.table_name]).scalar()

        # convert sqlalchemy query result to scalar
        result = query_result

        return result

    def insert_row(self, _data):
        """
        Добавить новую запись в хранилище

        Args:
            _data (Dict): структура данных для записи

        Returns:
            none
        """

        metadata = MetaData(bind=self.data_store)
        metadata.reflect()

        if _data.get('doc_id') is None:
            doc_id_last = self.get_rows(f'select max({metadata.tables[self.table_name].columns["doc_id"]}) from {self.table_name}')
            # _data['doc_id'] = max(data_list, key=lambda i: i['doc_id']) + 1
            _data['doc_id'] = doc_id_last[0]['max'] + 1

        result = self.data_store.execute(
            insert(metadata.tables[self.table_name]),[_data],
        )

        return _data['doc_id']

    '''
    def update_row(self, _data, _where):
        """
        Обновление данных

        Args:
            _data(Dict): структура данных для записи
            _where(Dict): переменная для поиска нужной записи
        """

        # self.data_store.update(_data, where(_where) == _data[_where])
        metadata = MetaData(bind=self.data_store)
        metadata.reflect()

        result = self.data_store.execute(
            update(metadata.tables[self.table_name]),[_data],
        )
    '''
    
    def update_row_by_id(self, _data, _id):
        """
        Обновление данных по id

        Args:
            _data(Dict): структура данных для записи
            _id(Int): id записи
        """

        metadata = MetaData(bind=self.data_store)
        metadata.reflect()

        result = self.data_store.execute(
            update(metadata.tables[self.table_name]).where(metadata.tables[self.table_name].columns["doc_id"] == _id),[_data],
        )
