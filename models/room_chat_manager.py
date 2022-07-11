from models.room_chat import RoomChat, Message
from data_adapters.data_store import DataStore
from datetime import datetime

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

        if _room_chat.get("id_education_stream") is not None:
            room_chat.id_education_stream = _room_chat.get("id_education_stream")
        else:
            room_chat.id_education_stream = ""

        return room_chat

    def message_row_to_message(self, _message):
        """
        Преобразует структуру данных, в которой хранится информация о сообщение в структуру Message

        Args:
            _message (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Message: пользователь
        """

        message = Message(_id=_message["id"], _name_sender=_message["name_sender"], _text=_message["text"])

        if _message.get("date_send") is not None:
            message.date_send = datetime.strptime(_message['date_end'], "%d/%m/%Y")
        else:
            message.date_send = datetime.today()

        return message

    def room_chat_entry(self, _id_lesson, _user, _id_course, _id_room_chat, _id_education_stream, _id_module):
        """
        Подключает пользователя к чату

        Args:
            _id_lesson(Int): индентификатор урока
            _user(User): данные пользователя
            _id_course(Int): индентификатор курса
            _id_room_chat(Int): индентификатор чата
            _id_education_stream(Int): индентификатор обучающего потока
        """

        data_store = DataStore("room_chat")

        if _id_room_chat is None:
            name_chat = "chat_{id_course}_{id_lesson}_{login_user}".format(
                id_lesson=_id_lesson, login_user=_user.login, id_course=_id_course)
            room_chat_list = data_store.get_rows({"name": name_chat})
        else:
            room_chat_list = data_store.get_rows({"id": int(_id_room_chat)})
            name_chat = room_chat_list[0]["name"]

        if room_chat_list == []:
            room_chat = self.add_room_chat(name_chat, _id_education_stream)
        elif _id_room_chat is None:
            room_chat = None
            for i_room_chat in room_chat_list:
                if i_room_chat.get("id_education_stream") is not None:

                    room_chat = self.room_chat_row_to_room_chat(i_room_chat)
                    break


        if len(room_chat_list) == 1:
            room_chat = self.room_chat_row_to_room_chat(room_chat_list[0])

        if room_chat is None:
            room_chat = self.add_room_chat(name_chat, _id_education_stream)

        if room_chat.message is not None:
            message_list = self.get_messages(room_chat.message)
            room_chat.message = message_list

        return room_chat

    def add_room_chat(self, _name_chat, _id_education_stream):
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
            "message": [],
            "id_education_stream": _id_education_stream
        }
        room_chat = self.room_chat_row_to_room_chat(room_chat)

        data_store.add_row({"id": room_chat.id, "name": room_chat.name, "message": [],
                            "id_education_stream": room_chat.id_education_stream})

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

            message_list.append(message)

        return message_list

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
        _message["send"] = datetime.today()
        message = self.message_row_to_message(_message)

        data_store_message.add_row({"id": message.id, "name_sender": message.name_sender, "text": message.text})

        data_store.update_messages(message.id, int(_id_room_chat))

        return message

    def get_room_chat(self, _id_room_chat):
        """
        Возвращает данные комнаты чата

        Args:
            _id_room_chat(Int): ID комнаты чата

        Return:
            RoomChat: комната чата
        """

        data_store = DataStore("room_chat")

        room_chat = data_store.get_rows({"id": _id_room_chat})[0]

        return self.room_chat_row_to_room_chat(room_chat)