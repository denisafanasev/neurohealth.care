from models.homework_chat import HomeworkChat
from data_adapters.data_store import DataStore


class HomeworkChatManager():
    """
    Класс модели управления комнатами чатов
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """

    def homework_chat_row_to_homework_chat(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о чате в структуру RoomChat

        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер

        Returns:
            HomeworkChat: чат
        """

        doc_id = _data_row['doc_id'] if _data_row.get('doc_id') is not None else _data_row.doc_id
        homework_chat = HomeworkChat(_id=doc_id, _id_lesson=_data_row['id_lesson'],
                                     _id_user=_data_row["id_user"])

        if _data_row.get('message') is not None:
            homework_chat.message = _data_row['message']

        if _data_row.get('unread_message_amount') is not None:
            homework_chat.unread_message_amount = _data_row['unread_message_amount']

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

        id_homework_chat = data_store.insert_row(
            {"id_user": homework_chat.id_user, "id_lesson": homework_chat.id_lesson})

        return id_homework_chat

    def get_homework_chat(self, _id_user, _id_lesson, _role):
        """
        Возвращает данные чата

        Args:
            _id_user(Int): ID пользователя
            _id_lesson(Int): ID урока

        Return:
            HomeworkChat: чата
        """

        data_store = DataStore("homework_chat", force_adapter='PostgreSQLDataAdapter')
        if data_store.is_there_model_data_in_sql_db():
            if _role == 'superuser':
                query_text = f'and message.id_user = {_id_user}'

            else:
                query_text = f'and message.id_user != {_id_user}'

            query = f"""with count_messages_user as (select count(*) over (partition by doc_id) as unread_message_amount, id_homework_chat
                                               from message
                                               where read is false {query_text })
                        select homework_chat.*, unread_message_amount, array_to_json(array_agg(message)) as message
                        from homework_chat,
                             message, count_messages_user
                        where homework_chat.doc_id = message.id_homework_chat
                          and homework_chat.id_user = {_id_user} and count_messages_user.id_homework_chat = homework_chat.doc_id
                          and homework_chat.id_lesson = {_id_lesson}
                        group by homework_chat.doc_id, id_lesson, homework_chat.id_user, unread_message_amount"""

            homework_chat = data_store.get_rows({'query': query})
            if homework_chat:
                return self.homework_chat_row_to_homework_chat(homework_chat[0])
        else:
            homework_chat = data_store.get_rows({"id_user": _id_user, "id_lesson": _id_lesson})

        if homework_chat:
            return self.homework_chat_row_to_homework_chat(homework_chat[0])

    def get_homework_chat_without_homework(self, _id_user: int, _id_course: int):
        """

        """
        data_store = DataStore('homework_chat', force_adapter='PostgreSQLDataAdapter')

        homework_chats_list_data = data_store.get_rows({
            'query': f"""
            WITH lesson AS (SELECT l.name       AS name_lesson,
                                   l.doc_id     AS doc_id_lesson,
                                   l.id_module  AS doc_id_module,
                                   modules.name AS name_module,
                                   modules.id_course
                            FROM (SELECT * FROM lessons WHERE task is not null) l
                                     LEFT JOIN modules ON l.id_module = modules.doc_id
                            WHERE modules.id_course = 1),
                 count_message AS (SELECT count(*) AS unread_message_amount, id_user id_user_message, id_homework_chat
                                   FROM message
                                   WHERE read IS FALSE
                                   group by id_homework_chat, id_user)
            SELECT chat_with_message.name_module,
                   chat_with_message.id_user,
                   chat_with_message.doc_id_lesson,
                   chat_with_message.doc_id,
                   chat_with_message.name_lesson,
                   chat_with_message.unread_message_amount,
                   chat_with_message.doc_id_module
            FROM homeworks
                     FULL JOIN (count_message RIGHT JOIN (homework_chat LEFT JOIN lesson
                                                          ON homework_chat.id_lesson = lesson.doc_id_lesson) chat
                                ON chat.doc_id = count_message.id_homework_chat) chat_with_message
                               ON homeworks.id_lesson = chat_with_message.id_lesson AND
                                  homeworks.id_user = chat_with_message.id_user
            
            WHERE chat_with_message.id_user = 272
              AND homeworks.doc_id IS NULL
              AND chat_with_message.name_module IS NOT NULL
            """
        })

        return homework_chats_list_data

    def is_there_homework_chat_in_sql_db(self) -> bool:
        """

        """
        data_store = DataStore('homework_chat', force_adapter='PostgreSQLDataAdapter')

        return data_store.is_there_model_data_in_sql_db()
