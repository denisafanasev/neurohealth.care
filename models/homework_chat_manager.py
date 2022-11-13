from models.homework_chat import HomeworkChat
from data_adapters.data_store import DataStore


class HomeworkChatManager():
    """
    Класс модели управления комнатами чатов
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """
    def homework_chat_row_to_homework_chat(self, _homework_chat):
        """
        Преобразует структуру данных, в которой хранится информация о чате в структуру RoomChat

        Args:
            _homework_chat (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            HomeworkChat: чат
        """

        homework_chat = HomeworkChat(_id=_homework_chat.doc_id, _id_lesson=_homework_chat['id_lesson'], _id_user=_homework_chat["id_user"])

        return homework_chat

    def homework_chat_entry(self, _id_homework_chat):
        """
        Подключает пользователя к чату

        Args:
            _id_homework_chat(Int): ID чата

        Returns:
            HomeworkChat: комната чата
        """

        data_store = DataStore("homework_chat")

        homework_chat_data = data_store.get_row_by_id(_id_homework_chat)
        if homework_chat_data is not None:
            return self.homework_chat_row_to_homework_chat(homework_chat_data)

    def add_homework_chat(self, _id_user: int, _id_lesson: int):
        """
        Создает новый чат

        Args:
            _id_user(Int): ID пользователя
            _id_lesson(Int): ID урока

        Return:
            HomeworkChat: чата
        """

        data_store = DataStore("homework_chat")

        homework_chat = HomeworkChat(_id_user=_id_user, _id_lesson=_id_lesson)

        id_homework_chat = data_store.insert_row({"id_user": homework_chat.id_user, "id_lesson": homework_chat.id_lesson})

        return id_homework_chat

    def get_homework_chat(self, _id_user, _id_lesson):
        """
        Возвращает данные чата

        Args:
            _id_user(Int): ID пользователя
            _id_lesson(Int): ID урока

        Return:
            HomeworkChat: чата
        """

        data_store = DataStore("homework_chat")

        homework_chat = data_store.get_rows({"id_user": _id_user, "id_lesson": _id_lesson})
        if homework_chat:
            return self.homework_chat_row_to_homework_chat(homework_chat[0])