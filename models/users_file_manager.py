import os

from models.users_file import UsersFile
from data_adapters.data_store import DataStore

class UsersFileManager():

    def user_files_row_to_users_files(self, _data_row):
        """
        Класс модели управления файлами пользователей
        Взаимодействует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
        Возвращает в слой бизнес-логики приложения объекты в доменных структурах
        """
        users_file = UsersFile(_name_file_user=_data_row["name_file_user"], _name_file_unique=_data_row["name_file_unique"],
                               _path=_data_row["path"])

        return users_file

    def get_users_file(self, _name_file_unique):
        """
        Возвращает данные о файле пользователя по уникальному имени файла

        Args:
            _name_file_unique(String): уникальное имя файла

        Returns:
            UsersFile: данные файла пользователя
        """
        data_store = DataStore("users_files")

        users_file = data_store.get_rows({"name_file_unique": _name_file_unique})

        return self.user_files_row_to_users_files(users_file[0])

    def get_users_files_list(self):
        """
        Возвращает все файлы, которые отправили пользователи

        Returns:
            users_files_list(List): список данных файлов пользователей
        """
        data_store = DataStore("users_files")

        users_files = data_store.get_rows()
        users_files_list = []
        for users_file in users_files:
            users_files_list.append(self.user_files_row_to_users_files(users_file))

        return users_files_list

    def save_users_file(self, _users_file):
        """
        Сохраняет данные о файле, который отправил пользователь

        Args:
            _users_file(Dict): Данные о файле

        Returns:
            None
        """
        data_store = DataStore("users_files")

        user_files = self.user_files_row_to_users_files(_users_file)

        data_store.insert_row({"name_file_user": user_files.name_file_user, "name_file_unique": user_files.name_file_unique,
                            "path": user_files.path})

    def get_size_files(self, _files_list):
        """
        Возвращает данные о файлах, которые прислал пользователь, с размерами этих файлов

        Args:
            _files_list(List): список с уникальными именами файлов, которые отправил пользователь

        Returns:
            List: список с UsersFile и размерами данных файлов
        """
        data_store = DataStore("users_files")

        file_list = []
        for name_file_unique in _files_list:
            file = data_store.get_rows({"name_file_unique": name_file_unique})[0]
            # если данные о файле найдены, то узнаем его размер и записываем в UsersFile
            if file:
               user_file = self.user_files_row_to_users_files(file)
               user_file.size = os.path.getsize(os.path.join(user_file.path, user_file.name_file_unique))
               file_list.append(user_file)
            else:
                continue

        return file_list