import sqlalchemy as db
from sqlalchemy import create_engine, text, func, Table
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

        self.data_store = create_engine("postgresql:" + config.PostgreSQLDataAdapter_connection_string())
        if _table_name is not None:
            self.table = Table(_table_name, MetaData(bind=self.data_store), autoload_with=self.data_store)

    def get_rows(self, _filter=None):
        """
        Возвращается записи, которые соответствуют заданному критерию из заданной таблицы в виде списка Dict

        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """
        #
        # metadata = MetaData(bind=self.data_store)
        # metadata.reflect()
        if _filter is not None:
            if not _filter.get('query'):
                if _filter.get('select') is None:
                    query = select(self.table)
                else:
                    query = select(text(_filter['select']))

                query = self.update_query(_filter, query)

            else:
                query = text(_filter['query'])

        else:
            query = select(self.table)

        query_result = self.data_store.execute(query)

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
            # run select by doc_id (default primary key for each table)
            query_result = self.data_store.execute(
                select(self.table).where(self.table.columns["doc_id"] == _id)
            )
            # convert sqlalchemy query result to list of dict
            result = [u._asdict() for u in query_result.all()]

            result = result[0] if result else None

        return result

    def get_rows_count(self, _filter=""):
        """
        Возвращается количество записей, которые соответствуют заданному критерию из заданной таблицы
        @params:
            _filter   - Optional  : срока с заданным фильтром (String)
        """
        query_result = db.select([db.func.count()]).select_from(self.table)
        if _filter:
            query_result = self.update_query(_filter, query_result)

        # convert sqlalchemy query result to scalar
        result = query_result.scalar()

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
            doc_id_last = self.data_store.execute(select(db.func.max(self.table.columns['doc_id']))).scalar()
            if doc_id_last is not None:
                _data['doc_id'] = doc_id_last + 1
            else:
                _data['doc_id'] = 1
        result = self.data_store.execute(
            insert(self.table), [_data],
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
            update(self.table).where(self.table.columns["doc_id"] == _id),
            [_data],
        )

    def update_query(self, _query_dict, _query):
        """
        Дополняет запрос к БД

        Args:
            _query_dict(Dict):
            _query(Query)

        Returns:
            _query(Query): Окончательный запрос
        """
        if _query_dict.get('where') is not None:
            _query = _query.where(text(_query_dict['where']))

        if _query_dict.get('group_by') is not None:
            _query = _query.group_by(text(_query_dict['group_by']))

        if _query_dict.get('order_by') is not None:
            _query = _query.order_by(text(_query_dict['order_by']))

        if _query_dict.get('having') is not None:
            _query = _query.having(text(_query_dict['having']))

        if _query_dict.get('limit') is not None:
            _query = _query.limit(_query_dict['limit'])

        if _query_dict.get('offset') is not None:
            _query = _query.offset(_query_dict['offset'])

        return _query

    def get_rows_by_query(self, _data):

        query_result = self.data_store.execute(text(_data))

        result = [u._asdict() for u in query_result.all()]

        return result