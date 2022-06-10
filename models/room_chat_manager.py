import os
import config

from models.room_chat import RoomChat, Message, UserFile
from data_adapters.data_store import DataStore

class RoomChatManager():

    def room_chat_row_to_room_chat(self, _room_chat):
        """
        Преобразует структуру данных, в которой хранится информация о чате в структуру RoomChat

        Args:
            _room_chat (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            RoomChat: пользователь
        """

        room_chat = RoomChat(_id=_room_chat["id"], _name=_room_chat["name"], _message=_room_chat["message"])

        return room_chat

    def message_row_to_message(self, _message):
        """
        Преобразует структуру данных, в которой хранится информация о сообщение в структуру Message

        Args:
            _message (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Message: пользователь
        """

        message = Message(_id=_message["id"], _name_sender=_message["name_sender"], _text=_message["text"],
                          _files=_message["files"])

        return message

    def file_row_to_file(self, _file):
        """
        Преобразует структуру данных, в которой хранится информация о файле в структуру File

        Args:
            _file (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            UserFile: пользователь
        """

        file = UserFile(_name_file_user=_file["name_file_user"], _name_file_unique=_file["name_file_unique"],
                        _path=_file["path"])

        return file

    def room_chat_entry(self, _id_lesson, _user, _id_course, _id_room_chat):
        """
        Подключает пользователя к чату

        Args:
            _id_lesson(Int): индентификатор урока
            _user(User): данные пользователя
            _id_course(Int): индентификатор курса
            _id_room_chat(Int): индентификатор чата
        """

        data_store = DataStore("room_chat")

        if _id_room_chat is None:
            name_chat = "chat_{id_course}_{id_lesson}_{login_user}".format(
                id_lesson=_id_lesson, login_user=_user.login, id_course=_id_course)
            room_chat = data_store.get_rows({"name": name_chat})
        else:
            room_chat = data_store.get_rows({"id": int(_id_room_chat)})
            name_chat = room_chat[0]["name"]

        if room_chat == []:
            if _user.role != "self_study":
                room_chat = self.add_room_chat(name_chat)
            else:
                room_chat = None
        else:
            room_chat = self.room_chat_row_to_room_chat(room_chat[0])
            if room_chat.message is not None:
                message_list = self.get_messages(room_chat.message)
                room_chat.message = message_list

        return room_chat

    def add_room_chat(self, _name_chat):
        """
        Создает новый чат

        Args:
            _name_chat(String): название чата
        """

        data_store = DataStore("room_chat")
        count_room_chat = data_store.get_rows_count()
        room_chat = {
            "id": count_room_chat + 1,
            "name": _name_chat,
            "message": []
        }
        room_chat = self.room_chat_row_to_room_chat(room_chat)

        data_store.add_row({"id": room_chat.id, "name": room_chat.name, "message": []})

        return room_chat

    def get_messages(self, _id_message_list):
        """
        Возвращает все сообщения из чата

        Args:
            _id_message_list(List): список индентификаторов сообщений
        """

        data_store_message = DataStore("message")
        message_list = []

        for i_message in _id_message_list:
            message = data_store_message.get_rows({"id": i_message})[0]
            message = self.message_row_to_message(message)

            if message.files is not None:
                files_list = self.get_files(message.files)
                message.files = files_list
            message_list.append(message)

        return message_list

    def get_files(self, _name_file_list):
        """
        Возвращает данные файлов из чата

        Args:
            _name_file_list(List): список уникальных имен файлов из чата
        """

        data_store_files = DataStore("files")
        files_list = []

        for i_file in _name_file_list:
            file = data_store_files.get_rows({"name_file_unique": i_file})[0]
            file = self.file_row_to_file(file)
            files_list.append(file)

        return files_list

    def add_message(self, _message, _id_room_chat):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
            _id_room_chat(Int): индентификатор чата
        """

        data_store = DataStore("room_chat")
        data_store_message = DataStore("message")
        amount = data_store_message.get_rows_count()

        _message["id"] = amount + 1
        message = self.message_row_to_message(_message)

        if message.files is not None:
            file_list = []
            for i_file in message.files:
                file = self.save_files(i_file)
                file_list.append(file.name_file_unique)
            message.files = file_list

        data_store_message.add_row({"id": message.id, "name_sender": message.name_sender, "text": message.text,
                                    "files": message.files})

        data_store.update_messages(message.id, int(_id_room_chat))


    def save_files(self, _file):
        """
        Сохраняет данные файла

        Args:
            _file(Dict): данные файла
        """

        data_store = DataStore("files")

        file = self.file_row_to_file({"name_file_user": _file["name_file_user"], "name_file_unique": _file["name_file_unique"], "path": _file["path"]})
        data_store.add_row({"name_file_user": file.name_file_user, "name_file_unique": file.name_file_unique, "path": file.path})

        return file