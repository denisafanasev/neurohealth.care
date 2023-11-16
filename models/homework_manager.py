from datetime import datetime

import pandas

from models.homework import Homework
from data_adapters.data_store import DataStore
from error import HomeworkManagerException


class HomeworkManager:
    """
    Класс модели управления домашними работами
    Взаимодейтвует с модулем хранения данных, преобразую доменные структуры в объекты типа Dict
    Вовзращает в слой бизнес-логики приложения объекты в доменных структурах
    """

    def homework_row_to_homework(self, _data_row):
        """
        Преобразует структуру данных, в которой хранится информация о домашней работе в структуру Homework
        Args:
            _data_row (Dict): структура данных, которую возвращает дата адаптер
        Returns:
            Homework: домашняя работа
        """
        doc_id = _data_row['doc_id'] if _data_row.get('doc_id') is not None else _data_row.doc_id
        homework = Homework(_id=doc_id, _users_files_list=_data_row['users_files_list'],
                            _text=_data_row['text'], _id_lesson=_data_row['id_lesson'], _id_user=_data_row['id_user'],
                            _status=_data_row['status'])

        if _data_row.get('created_date') is not None:
            if isinstance(_data_row['created_date'], str):
                homework.date_delivery = datetime.strptime(_data_row['date_delivery'], "%d/%m/%Y")
            else:
                homework.date_delivery = _data_row['date_delivery']
        else:
            homework.date_delivery = datetime.today()

        return homework

    def create_homework(self, _homework_files_list, _text, _id_user, _id_lesson):
        """
        Сохраняет домашнюю работу

        Args:
            _homework_files_list(Dict): данные сданной домашней работы
            _text(String): ответ на задание
            _id_user(Int): ID пользователя
            _id_lesson(Int): ID урока

        Return:
            Homework: домашняя работа
        """

        data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')

        homework = Homework(_users_files_list=_homework_files_list, _text=_text, _id_user=_id_user,
                            _id_lesson=_id_lesson, _status=None, _date_delivery=datetime.now())

        data_store.insert_row({"users_files_list": homework.users_files_list,
                               "date_delivery": homework.date_delivery.strftime("%d/%m/%Y"), "text": homework.text,
                               "id_user": homework.id_user, "id_lesson": homework.id_lesson, "status": homework.status})

    def get_homeworks(self):
        """
        Возвращает список домашних работ пользователей

        Returns:
            List: список домашних работ
        """

        data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')

        homeworks = data_store.get_rows()
        homework_list = []
        for homework in homeworks:
            homework_list.append(self.homework_row_to_homework(homework))

        return homework_list

    def get_homeworks_list_by_id_lesson_no_verified(self, _id_lesson, _id_user):
        """
        Возвращает список непроверенных домашних работ по ID урока и ID пользователя

        Args:
            _id_lesson(Int): ID урока
            _id_user(Int): ID пользователя

        Return:
            List: список домашних работ
        """

        data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')
        if data_store.is_there_model_data_in_sql_db():
            homeworks_list = data_store.get_rows(
                {
                    "where": "id_lesson = {_id_lesson} and id_user = {_id_user} and status is null".format(
                        _id_lesson=_id_lesson,
                        _id_user=_id_user
                    )
                }
            )

        else:
            homeworks_list = data_store.get_rows({"id_lesson": _id_lesson, "id_user": _id_user, 'status': None})

        homeworks = []
        for homework in homeworks_list:
            homeworks.append(self.homework_row_to_homework(homework))

        return homeworks

    def get_homeworks_list_by_id_lessons_list_no_verified(self, _id_lessons_list: list, _id_user: int) -> list:
        """
        Возвращает список домашних работ пользователя по урокам из списка

        Args:
            _id_lessons_list: список ID уроков
            _id_user: ID пользователя

        Returns:
            homeworks: список непроверенных домашних работ
        """

        data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')
        if data_store.is_there_model_data_in_sql_db():
            homework_list = data_store.get_rows({
                'query': f"""
                select *
                from homeworks
                left outer join (select lessons.name   as name_lesson,
                                    lessons.doc_id as doc_id_lesson,
                                    modules.doc_id as doc_id_module,
                                    id_module,
                                    modules.name   as name_module
                                from lessons
                                left outer join modules on lessons.id_module = modules.doc_id) as lesson
                         on homeworks.id_lesson = lesson.doc_id_lesson
                where id_lesson IN (SELECT unnest(ARRAY[{_id_lessons_list}])) AND id_user = {_id_user} AND status IS NULL
                         """,
            })

            return homework_list

    def get_homeworks_list_by_id_lessons_list_verified(self, _id_course: int, _id_user: int) -> list:
        """
        Возвращает список домашних работ пользователя по урокам из списка

        Args:
            _id_course: список ID уроков
            _id_user: ID пользователя

        Returns:
            homeworks: список непроверенных домашних работ
        """
        data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')
        if data_store.is_there_model_data_in_sql_db():
            homework_list = data_store.get_rows({
                'query': f"""
                select *
                from homeworks
                left outer join (select lessons.name   as name_lesson,
                                    lessons.doc_id as doc_id_lesson,
                                    modules.doc_id as doc_id_module,
                                    id_module,
                                    modules.name   as name_module,
                                    modules.id_course
                                from lessons
                                left outer join modules on lessons.id_module = modules.doc_id) as lesson
                         on homeworks.id_lesson = lesson.doc_id_lesson
                where id_course = {_id_course} AND id_user = {_id_user} AND status IS NOT NULL
                         """,
            })

            return homework_list

    def get_homeworks_list_by_id_lesson(self, _id_lesson, _id_user):
        """
        Возвращает список домашних работ по ID урока и ID пользователя

        Args:
            _id_lesson(Int): ID урока
            _id_user(Int): ID пользователя

        Return:
            List: список домашних работ
        """
        data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')
        if data_store.is_there_model_data_in_sql_db():
            homeworks_list = data_store.get_rows(
                {"where": f"id_lesson = {_id_lesson} and id_user = {_id_user}".format(
                    _id_lesson=_id_lesson,
                    _id_user=_id_user
                )})
        else:
            homeworks_list = data_store.get_rows({"id_lesson": _id_lesson, "id_user": _id_user})

        homeworks = []
        for homework in homeworks_list:
            homeworks.append(self.homework_row_to_homework(homework))

        if homeworks:
            return homeworks

    def get_homework_by_id(self, _id):
        """
        Возвращает домашнюю работу по ID

        Args:
            _id(Int): ID домашней работы

        Return:
            Homework: домашняя работа
        """

        data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')

        homework = data_store.get_row_by_id(_id)
        if homework is not None:
            return self.homework_row_to_homework(homework)

    def homework_answer_accepted(self, _id_homework):
        """
        Меняет статус проверки домашней работы на "Принято"

        Args:
            _id_homework(Int): ID домашней работы

        Returns:
            Homework: домашняя работа
        """
        data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')

        data_store.update_row_by_id({"status": True}, _id_homework)
        homework = data_store.get_row_by_id(_id_homework)

        return self.homework_row_to_homework(homework)

    def homework_answer_no_accepted(self, _id_homework):
        """
        Меняет статус проверки домашней работы на "Не принято"

        Args:
            _id_homework(Int): ID домашней работы

        Returns:
            Homework: домашняя работа
        """

        data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')

        data_store.update_row_by_id({"status": False}, _id_homework)
        homework = data_store.get_row_by_id(_id_homework)

        return self.homework_row_to_homework(homework)

    def is_accepted_homework(self, _user_id, _id_lesson):
        """
        Проверяет, есть ли принятые домашние работы у пользователя.(Если используется в качестве БД TinyDB)

        Args:
            _user_id(Int): ID пользователя
            _id_lesson(Int): ID урока

        Returns:
            Если есть, возвращает True, иначе False
        """
        homework_list = self.get_homeworks_list_by_id_lesson(_id_lesson, _user_id)
        if homework_list is not None:
            for homework in homework_list:
                if homework.status is True:
                    return True

        return False

    def get_count_accepted_homework_for_lessons_id(self, _user_id: int, _id_course: int):
        """
        (Если используется в качестве БД PostgreSQL)
        """
        data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')

        data = data_store.get_rows({
            'query':
                f"""
                with lesson as (select lessons.doc_id,
                                   modules.doc_id as                           module_doc_id,
                                   count(*) over (partition by modules.doc_id) count_lessons_in_module
                            from lessons
                                     join modules on lessons.id_module = modules.doc_id
                            where modules.id_course = {_id_course}
                              and lessons.task is not null),
                     homework as (select count(*) AS                   count_homework_in_module,
                                         (select count(*) from lesson) count_lessons,
                                         lesson.module_doc_id,
                                         count_lessons_in_module
                                  from homeworks
                                           join lesson
                                                on homeworks.id_lesson = lesson.doc_id
                                  where id_user = {_user_id}
                                    AND status is true
                                  group by lesson.module_doc_id, count_lessons_in_module)
                select count_lessons,
                       (select sum(count_homework_in_module) from homework) as sum_homework,
                       count(module_doc_id) as count_modules_passed
                from homework
                group by count_lessons
                """
        })

        return data

    def get_id_lessons_list_with_completed_homework(self, _user_id):
        """
        Возвращает множество из ID уроков, по которым приняты домашние работы у пользователя

        Args:
            _user_id(Int): ID пользователя

        Returns:
            Set(Homework): список принятых домашних работ
        """
        if self.is_there_homework_in_sql_db():
            data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')

            homeworks_list_data = data_store.get_rows({'where': f'id_user = {_user_id} and status is True'.format(
                _user_id=_user_id
            )})
        else:
            data_store = DataStore('homeworks')

            homeworks_list_data = data_store.get_rows({'id_user': _user_id, 'status': True})

        id_lessons_list = set()
        if homeworks_list_data:
            for homework_data in homeworks_list_data:
                id_lessons_list.add(homework_data['id_lesson'])

        return id_lessons_list

    def is_there_homework_in_sql_db(self) -> bool:
        """

        """
        data_store = DataStore('homeworks', force_adapter='PostgreSQLDataAdapter')

        return data_store.is_there_model_data_in_sql_db()
