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

        message = Message(_id=_message.doc_id, _text=_message["text"], _id_homework_chat=_message['id_homework_chat'],
                          _id_user=_message['id_user'])

        if _message.get("date_send") is not None:
            message.date_send = datetime.strptime(_message['date_send'], "%d/%m/%Y")
        else:
            message.date_send = datetime.today()

        if _message.get("read") is not None:
            message.read = _message['read']

        return message

    def get_messages(self, _id_homework_chat, _id_user):
        """
        Возвращает все сообщения из чата по ID комнаты чата

        Args:
            _id_homework_chat(Int): ID комнаты чата
            _id_user(Int): ID текущего пользователя

        Return:
            List: список сообщений чата
        """

        data_store = DataStore("message")

        messages_data = data_store.get_rows({"id_homework_chat": _id_homework_chat})
        message_list = []
        for i_message in messages_data:
            message = self.message_row_to_message(i_message)
            if not message.read:
                # если сообщение отправил не текущий пользователь, то отмечается как прочитанное
                if message.id_user != _id_user:
                    message.read = True
                    data_store.update_row_by_id({"read": True}, message.id)

            message_list.append(message)

        return message_list

    def add_message(self, _message):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения

        Return:
            Message: сообщение
        """

        data_store = DataStore("message")

        _message["date_send"] = datetime.now()
        message = Message(_id_user=_message['id_user'], _id_homework_chat=int(_message['id_homework_chat']),
                          _text=_message['text'], _date_send=_message['date_send'])

        data_store.insert_row({"text": message.text, "id_user": message.id_user,
                            "id_homework_chat": message.id_homework_chat, "date_send": _message['date_send'].strftime("%d/%m/%Y"),
                            "read": message.read})

        return message

    def get_unread_messages_amount(self, _id_homework_chat, _id_user):
        """
        Возвращает количество непрочитанных сообщений

        Args:
            _id_homework_chat(Integer): ID комнаты чата
            _id_user(Integer): ID текущего пользователя

        Return:
            Integer: количество непрочитанных сообщений
        """
        data_store = DataStore("message")

        messages_data_list = data_store.get_rows({"read": False, "id_homework_chat": _id_homework_chat})
        amount = 0
        for message_data in messages_data_list:
            if message_data['id_user'] != _id_user:
                amount += 1

        return amount