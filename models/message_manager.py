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

        message = Message(_id=_message.doc_id, _text=_message["text"], _id_room_chat=_message['id_room_chat'])

        if _message.get("date_send") is not None:
            message.date_send = datetime.strptime(_message['date_end'], "%d/%m/%Y")
        else:
            message.date_send = datetime.today()

        return message

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

        data_store = DataStore("message")
        amount = data_store.get_rows_count()

        _message["id"] = amount + 1
        _message["date_send"] = datetime.today()
        message = self.message_row_to_message(_message)

        data_store.add_row({"id": message.id, "text": message.text})

        return message