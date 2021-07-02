from tinydb import TinyDB, Query, where

class DataStore():
    """
    Класс предназначен для работы с системой хранения данных
    Возвращается структуры типа Dict, а хранит данные в том виде
    в котором это предполагает используемый адаптер

    для разных структур может использовать разные адаптеры

    поддерживаемые системы хранения: TinyDB
    """

    data_store = None

    def __init__(self, _type):
        """
        Возвращается объект хранилища данных по указанному типу данных
        @params:
            _type    - Required  : тип данных (String)
        """
        
        self.data_store = TinyDB("data/" + _type + ".json")


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
        Возвращается поличество записей, которые соответствуют заданному критерию из заданной таблицы
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