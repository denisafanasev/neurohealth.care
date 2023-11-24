from datetime import datetime

from data_adapters.data_store import DataStore
from models.message import Message


class MessageManager():
    """
    Класс модели управления сообщениями
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """
    def message_row_to_message(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о сообщение в структуру Message

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            Message: пользователь
        """
        doc_id = _data_row['doc_id'] if _data_row.get('doc_id') is not None else _data_row.doc_id
        message = Message(_id=doc_id, _text=_data_row["text"], _id_homework_chat=_data_row['id_homework_chat'],
                          _id_user=_data_row['id_user'])

        if _data_row.get("date_send") is not None:
            if isinstance(_data_row["date_send"], str):
                # "%d/%m/%Y"
                message.date_send = datetime.strptime(_data_row['date_send'], '%Y-%m-%dT%H:%M:%S')
            else:
                message.date_send = _data_row['date_send']
        else:
            message.date_send = datetime.today()

        if _data_row.get("read") is not None:
            message.read = _data_row['read']

        return message

    def get_messages_for_user(self, _id_homework_chat, _id_user):
        """
        Возвращает все сообщения из чата по ID комнаты чата

        Args:
            _id_homework_chat(Int): ID комнаты чата
            _id_user(Int): ID текущего пользователя

        Return:
            List: список сообщений чата
        """

        data_store = DataStore("message", force_adapter='PostgreSQLDataAdapter')

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

    def get_messages_for_superuser(self, _id_homework_chat, _id_user):
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
                if message.id_user == _id_user:
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

        data_store = DataStore("message", force_adapter='PostgreSQLDataAdapter')

        _message["date_send"] = datetime.now()
        message = Message(_id_user=_message['id_user'], _id_homework_chat=_message['id_homework_chat'],
                          _text=_message['text'], _date_send=_message['date_send'])
        if not data_store.is_there_model_data_in_sql_db():
            _message['date_send'] = _message['date_send'].strftime("%d/%m/%Y")
        else:
            _message['date_send'] = _message['date_send'].date()

        data_store.insert_row({"text": message.text, "id_user": message.id_user,
                            "id_homework_chat": message.id_homework_chat, "date_send": _message['date_send'],
                            "read": message.read})

        return message

    def get_unread_messages_amount_for_user(self, _id_homework_chat, _id_user):
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

    def get_unread_messages_amount_for_superuser(self, _id_homework_chat, _id_user):
        """
        Возвращает количество непрочитанных сообщений

        Args:
            _id_homework_chat(Integer): ID комнаты чата
            _id_user(Integer): ID текущего пользователя

        Return:
            Integer: количество непрочитанных сообщений
        """
        data_store = DataStore("message")

        amount_unread_messages = data_store.get_rows_count({"read": False, "id_user": _id_user, "id_homework_chat": _id_homework_chat})

        return amount_unread_messages

    def get_unread_messages_by_id_user(self, _id_user):
        """
        Возвращает список непрочитанных суперпользователями сообщений от пользователя

        Args:
            _id_user(Int): ID пользователя

        Return:
            unread_messages_list(List(Message)): список непрочитанных сообщений
        """
        data_store = DataStore('message')

        unread_messages_data_list = data_store.get_rows({'read': False, 'id_user': _id_user})

        unread_messages_list = [self.message_row_to_message(unread_message) for unread_message in unread_messages_data_list]

        return unread_messages_list