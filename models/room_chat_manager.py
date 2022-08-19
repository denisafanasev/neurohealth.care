from models.room_chat import RoomChat
from models.message import Message
from data_adapters.data_store import DataStore
from datetime import datetime

class RoomChatManager():
    """
    Класс модели управления комнатами чатов
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """
    def room_chat_row_to_room_chat(self, _room_chat):
        """
        Преобразует структуру данных, в которой хранится информация о чате в структуру RoomChat

        Args:
            _room_chat (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            RoomChat: пользователь
        """

        room_chat = RoomChat(_id=_room_chat.doc_id, _id_lesson=_room_chat['id_lesson'], _id_user=_room_chat["id_user"])

        if _room_chat.get("id_education_stream") is not None:
            room_chat.id_education_stream = _room_chat.get("id_education_stream")
        else:
            room_chat.id_education_stream = ""

        return room_chat

    def room_chat_entry(self, _id_room_chat):
        """
        Подключает пользователя к чату

        Args:
            _id_lesson(Int): ID урока
            _id_user(User): ID пользователя
        """

        data_store = DataStore("room_chat")

        room_chat_data = data_store.get_row_by_id(_id_room_chat)
        if room_chat_data is not None:
            return self.room_chat_row_to_room_chat(room_chat_data)

    def add_room_chat(self, _id_user, _id_lesson):
        """
        Создает новый чат

        Args:
            _id_user(Int): ID пользователя
            _id_lesson(Int): ID урока

        Return:
            RoomChat: комната чата
        """

        data_store = DataStore("room_chat")

        room_chat = RoomChat(_id_user=_id_user, _id_lesson=_id_lesson)

        data_store.add_row({"id_user": room_chat.id_user, "id_lesson": room_chat.id_lesson})

        return room_chat

    def get_room_chat(self, _id_user, _id_lesson):
        """
        Возвращает данные комнаты чата

        Args:
            _id_user(Int): ID пользователя
            _id_lesson(Int): ID урока

        Return:
            RoomChat: комната чата
        """

        data_store = DataStore("room_chat")

        room_chat = data_store.get_rows({"id_user": _id_user, "id_lesson": _id_lesson})
        if room_chat != []:
            return self.room_chat_row_to_room_chat(room_chat[0])

    def get_room_chat_by_id(self, _id_room_chat):
        """
        Возвращает данные комнаты чата по ID

        Args:
            _id_room_chat(Int): ID комнаты чата

        Return:
            RoomChat: комната чата
        """

        data_store = DataStore("room_chat")

        room_chat = data_store.get_row_by_id(_id_room_chat)
        if room_chat is not None:
            return self.room_chat_row_to_room_chat(room_chat)
