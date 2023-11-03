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

    def get_homework_chat_without_homework(self, _id_user: int, _id_lessons_list: list):
        """

        """
        data_store = DataStore('homework_chat', force_adapter='PostgreSQLDataAdapter')

        homework_chats_list_data = data_store.get_rows({
            'query': f"""
            WITH lesson AS (SELECT l.name         AS name_lesson,
                       l.doc_id       AS doc_id_lesson,
                       l.id_module,
                       modules.name   AS name_module
                FROM (SELECT * FROM lessons WHERE task is not null) l
                         LEFT JOIN modules ON l.id_module = modules.doc_id),
     count_message AS (SELECT count(*) AS count_unread_message, id_user id_user_message, id_homework_chat
                       FROM message
                       WHERE read IS FALSE
                       group by id_homework_chat, id_user)
SELECT chat_with_message.name_module, chat_with_message.id_user, chat_with_message.id_lesson, chat_with_message.doc_id,
       chat_with_message.name_lesson, chat_with_message.count_unread_message, chat_with_message.id_module,
       homeworks.doc_id AS doc_id_home
FROM homeworks
         FULL JOIN (count_message RIGHT JOIN (homework_chat LEFT JOIN lesson
                                              ON homework_chat.id_lesson = lesson.doc_id_lesson) chat
                    ON chat.doc_id = count_message.id_homework_chat) chat_with_message
                   ON homeworks.id_lesson = chat_with_message.id_lesson AND homeworks.id_user = chat_with_message.id_user

WHERE chat_with_message.id_user = {_id_user}
  AND homeworks.doc_id IS NULL
            """
        })

        return homework_chats_list_data