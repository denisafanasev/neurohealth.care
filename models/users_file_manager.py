import os

from models.users_file import UsersFile
from data_adapters.data_store import DataStore

class UsersFileManager():

    def user_files_row_to_users_files(self, _data_row):

        users_file = UsersFile(_name_file_user=_data_row["name_file_user"], _name_file_unique=_data_row["name_file_unique"],
                               _path=_data_row["path"])

        return users_file

    def get_users_file(self, _name_file_unique):

        data_store = DataStore("users_files")

        users_file = data_store.get_rows({"name_file_unique": _name_file_unique})

        return self.user_files_row_to_users_files(users_file[0])

    def get_users_files_list(self):

        data_store = DataStore("users_files")

        users_files = data_store.get_rows()
        users_files_list = []
        for users_file in users_files:
            users_files_list.append(self.user_files_row_to_users_files(users_file))

        return users_files_list

    def save_users_file(self, _users_file):

        data_store = DataStore("users_files")

        user_files = self.user_files_row_to_users_files(_users_file)

        data_store.insert_row({"name_file_user": user_files.name_file_user, "name_file_unique": user_files.name_file_unique,
                            "path": user_files.path})

    def get_size_files(self, _files_list):

        data_store = DataStore("users_files")

        file_list = []
        for name_file_unique in _files_list:
            try:
                file = data_store.get_rows({"name_file_unique": name_file_unique})[0]
                if file:
                   user_file = self.user_files_row_to_users_files(file)
                   user_file.size = os.path.getsize(os.path.join(user_file.path, user_file.name_file_unique))
                   file_list.append(user_file)
                else:
                    continue

            except FileNotFoundError:
                file_list = None

        return file_list