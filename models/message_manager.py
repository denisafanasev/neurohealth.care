from datetime import datetime

from data_adapters.data_store import DataStore
from models.message import Message


class MessageManager():
    """
    Класс модели управления сообщениями
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """
    def message_row_to_message(self, _message):
        """
        Преобразует структуру данных, в которой хранится информация о сообщение в структуру Message

        Args:
            _message (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Message: пользователь
        """

        message = Message(_id=_message.doc_id, _text=_message["text"], _id_room_chat=_message['id_room_chat'],
                          _id_user=_message['id_user'])

        if _message.get("date_send") is not None:
            message.date_send = datetime.strptime(_message['date_send'], "%d/%m/%Y")
        else:
            message.date_send = datetime.today()

        return message

    def get_messages(self, _id_room_chat):
        """
        Возвращает все сообщения из чата по ID комнаты чата

        Args:
            _id_room_chat(Int): ID комнаты чата

        Return:
            List: список сообщений чата
        """

        data_store = DataStore("message")

        messages_data = data_store.get_rows({"id_room_chat": _id_room_chat})
        message_list = []
        for i_message in messages_data:
            message = self.message_row_to_message(i_message)

            message_list.append(message)

        return message_list

    def add_message(self, _message):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
        """

        data_store = DataStore("message")

        _message["date_send"] = datetime.today()
        message = Message(_id_user=_message['id_user'], _id_room_chat=_message['id_room_chat'], _text=_message['text'])

        data_store.add_row({"text": message.text, "id_user": message.id_user,
                            "id_room_chat": message.id_room_chat, "date_send": _message['date_send'].strftime("%d/%m/%Y")})

        return message