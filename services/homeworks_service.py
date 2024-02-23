from typing import Union

import pandas as pd

import config
from models.homework_chat import HomeworkChat
from models.homework_manager import HomeworkManager
from models.course_manager import EducationCourseManager
from models.lesson import Lesson
from models.module import Module
from models.module_manager import EducationModuleManager
from models.lesson_manager import EducationLessonManager
from models.education_stream_manager import EducationStreamManager
from models.user_manager import UserManager
from models.homework_chat_manager import HomeworkChatManager
from models.message_manager import MessageManager


class HomeworksService():
    """
    HomeworksService - класс бизнес-логики сервиса управления настройками приложения.
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def get_lesson(self, _id_lesson):
        """
        Возвращает данные урока

        Args:
            _id_lesson(Int): id урока

        Returns:
            Lesson: урок
        """

        lesson_manager = EducationLessonManager()
        module_manager = EducationModuleManager()

        lesson = lesson_manager.get_lesson_by_id(_id_lesson)
        module = module_manager.get_module_by_id(lesson.id_module)
        module.lessons = lesson

        return module

    def get_education_stream(self, _id_education_stream):
        """
        Возвращает данные обучающего потока по его ID

        Args:
            _id_education_stream(Int): ID

        Returns:
            EducationStream: обучающий поток
        """

        education_stream_manager = EducationStreamManager()
        user_manager = UserManager()
        course_manager = EducationCourseManager()

        education_stream = education_stream_manager.get_education_stream(_id_education_stream)
        students_list = []
        for user_id in education_stream.students_list:
            user = user_manager.get_user_by_id(user_id)
            if user is not None:
                students_list.append(user)

        education_stream.students_list = students_list
        education_stream.course = course_manager.get_course_by_id(education_stream.course)

        return education_stream

    def get_user_by_id(self, _id_user):
        """
        Возвращает данные пользователя по ID

        Args:
            _id_user(Int): ID пользователя

        Returns:
            User: пользователь
        """

        user_manager = UserManager()

        return user_manager.get_user_by_id(_id_user)

    def get_homework_chat(self, _id_lesson, _id_user, _id_current_user):
        """
        Возвращает данные чата

        Args:
            _id_lesson(Integer): ID урока
            _id_user(Integer): ID пользователя
            _id_current_user(Integer): ID текущего пользователя

        Returns:
            RoomChat: комната чата
        """

        homework_chat_manager = HomeworkChatManager()
        message_manager = MessageManager()
        user_manager = UserManager()

        current_user_role = user_manager.get_user_role(_id_current_user)
        homework_chat = homework_chat_manager.get_homework_chat(_id_user, _id_lesson, current_user_role)
        if homework_chat is not None:
            if not homework_chat_manager.is_there_homework_chat_in_sql_db():
                homework_chat.unread_message_amount = message_manager.get_unread_messages_amount_for_superuser(
                    homework_chat.id, _id_user)

        return homework_chat

    def get_homework_chat_by_course(self, _course_id, _id_user, _id_current_user):
        """
        Возвращает данные чата

        Args:
            _course_id(Integer): ID урока
            _id_user(Integer): ID пользователя
            _id_current_user(Integer): ID текущего пользователя

        Returns:
            RoomChat: комната чата
        """

        homework_chat_manager = HomeworkChatManager()
        message_manager = MessageManager()
        user_manager = UserManager()

        current_user_role = user_manager.get_user_role(_id_current_user)
        homework_chat = homework_chat_manager.get_user_homework_chat_by_course(_id_user, _course_id, current_user_role)
        if homework_chat is not None:
            if not homework_chat_manager.is_there_homework_chat_in_sql_db():
                homework_chat.unread_message_amount = message_manager.get_unread_messages_amount_for_superuser(
                    homework_chat.id, _id_user)

        return homework_chat

    def get_users_list_in_education_streams_file(self, _id_education_stream):
        """
        Возвращает список пользователей, которые находятся в обучающем потоке

        Returns:
            List: список пользователей
        """
        user_manager = UserManager()

        users_login_list = []
        with open(config.DATA_FOLDER + f'course_1/s{_id_education_stream}_users.txt') as f:
            users_login_list.extend(f.read().splitlines())

        users_list = []
        for user_login in users_login_list:
            user = user_manager.get_user_by_login(user_login)
            if user is not None:
                users_list.append(user)

        return users_list

    def get_homeworks_chats_list_by_id_user(self, _id_course, _id_user):
        """
        Возвращает список проверенных домашних работ по ID пользователя и урока

        Args:
            _id_course(Integer): ID урока
            _id_user(Integer): ID пользователя

        Returns:
            List: список домашних работ
        """
        homework_chat_manager = HomeworkChatManager()

        # lessons_list = self.get_lessons_by_id_course(_id_course)
        # id_lessons_list = [lesson.id for lesson in lessons_list]
        homeworks_chat_list_data = homework_chat_manager.get_homework_chat_without_homework(_id_user, _id_course)
        # homeworks_chat_list = []
        # for homeworks_chat in homeworks_chat_list_data:
        #     homeworks_chat_list.append({
        #         'homeworks_chat': {'id': homeworks_chat['doc_id'], 'id_user': homeworks_chat['id_user'],
        #                            'id_lesson': homeworks_chat['id_lesson'],
        #                            'unread_message_amount': homeworks_chat['count_unread_message']},
        #         'lesson': {'doc_id': homeworks_chat['id_lesson'], 'name': homeworks_chat['name_lesson'],
        #                    'id_module': homeworks_chat['id_module']},
        #         'module': {'doc_id': homeworks_chat['id_module'], 'name': homeworks_chat['name_module'],
        #                    'id_course': _id_course}
        #     })

        return homeworks_chat_list_data

    def get_homeworks_list_by_id_user_verified(self, _id_user: int, _id_course: int = None,
                                               _id_lesson: int = None) -> pd.DataFrame:
        """
        Возвращает список проверенных домашних работ по ID пользователя и урока

        Args:
            _id_course(Integer): ID курса
            _id_user(Integer): ID пользователя
            _id_lesson: ID урока

        Returns:
            List: список домашних работ
            """
        homework_manager = HomeworkManager()

        if _id_course is not None:
            homework_list_data = homework_manager.get_homeworks_list_by_id_lessons_list_verified(_id_course,
                                                                                                 _id_user)
            # homework_list = []
            # for homework_data in homework_list_data:
            #     homework = {'homework': {'doc_id': homework_data['doc_id'], 'status': homework_data['status'],
            #                              'date_delivery': homework_data['date_delivery']},
            #                 'lesson': {'doc_id': homework_data['doc_id_lesson'], 'name': homework_data['name_lesson'],
            #                            'id_module': homework_data['id_module']},
            #                 'module': {'doc_id': homework_data['doc_id_module'], 'name': homework_data['name_module'],
            #                            'id_course': _id_course}}
            #
            #     homework_list.append(homework)

            return homework_list_data

        elif _id_lesson is not None:
            homework_list = homework_manager.get_homeworks_list_by_id_lesson(_id_lesson, _id_user)
            if homework_list:
                homeworks = [homework for homework in homework_list if homework.status is not None]
                return homeworks

    def get_homeworks_list_by_id_user_no_verified(self, _id_course: int, _id_user: int):
        """
        Возвращает список не проверенных домашних работ по ID пользователя и урока

        Args:
            _id_course(Integer): ID урока
            _id_user(Integer): ID пользователя

        Returns:
            homework_list: список домашних работ
        """
        homework_manager = HomeworkManager()

        lessons_list = self.get_lessons_by_id_course(_id_course)
        id_lessons_list = [lesson.id for lesson in lessons_list]
        homework_list_data = homework_manager.get_homeworks_list_by_id_lessons_list_no_verified(id_lessons_list,
                                                                                                _id_user)
        # homework_list = []
        # for homework_data in homework_list_data:
        #     homework = {'homework': homework_manager.homework_row_to_homework(homework_data),
        #                 'lesson': Lesson(_id=homework_data['doc_id_lesson'], _name=homework_data['name_lesson'],
        #                                  _id_module=homework_data['id_module']),
        #                 'module': Module(_id=homework_data['doc_id_module'], _name=homework_data['name_module'],
        #                                  _id_course=_id_course)}

        # homework_list.append(homework)

        return homework_list_data

    def get_lessons_by_id_course(self, _id_course):
        """
        Возвращает все уроки курса, у которых есть задание

        Return:
            List(Lesson): список уроков
        """
        lesson_manager = EducationLessonManager()
        module_manager = EducationModuleManager()

        modules_list = module_manager.get_course_modules_list(_id_course)
        lessons_list = []
        for module in modules_list:
            lessons_list_data = lesson_manager.get_lessons_list_by_id_module(module.id)
            lessons_list_with_task = [lesson for lesson in lessons_list_data if lesson.task is not None]
            lessons_list.extend(lessons_list_with_task)

        return lessons_list

    def get_module_by_id(self, _id):
        """
        Возвращает данные модуля по ID

        Args:
            _id(Int): ID модуля

        Return:
            Module: модуль
        """

        module_manager = EducationModuleManager()

        return module_manager.get_module_by_id(_id)

    def get_course_by_id(self, _id):
        """
        Возвращает данные курса по ID

        Args:
            _id(Int): ID курса

        Return:
            Course: курс
        """

        course_manager = EducationCourseManager()

        return course_manager.get_course_by_id(_id)

    def get_educations_stream(self):
        """
        Возвращает список всех обучающих потоков

        Returns:
            List(EducationStream): список образовательных потоков
        """

        education_stream = EducationStreamManager()

        return education_stream.get_education_streams()

    def is_unread_messages(self, _id_lessons_list: list, _user_id: int, _course_id: int = None):
        """
        Проверяет на наличие непрочитанных суперпользователями сообщений.
        Args:
            _id_lessons_list(Int): список ID уроков курса
            _user_id(Int): ID пользователя
            _course_id: ID курса

        Return:
            True - если есть хотя одно непрочитанное сообщение
            False - если нет непрочитанных сообщений
        """
        homework_chat_manager = HomeworkChatManager()
        message_manager = MessageManager()

        unread_messages_list = message_manager.get_unread_messages_by_id_user(_user_id, _course_id)
        if not homework_chat_manager.is_there_homework_chat_in_sql_db():
            for unread_message in unread_messages_list:
                homework_chat = homework_chat_manager.homework_chat_entry(unread_message.id_homework_chat)
                if homework_chat.id_lesson in _id_lessons_list:
                    return True

            return False

        return unread_messages_list

    def get_amount_accepted_homework(self, _user_id: int, _id_lessons_list: list, _id_course: int = None):
        """
        Возвращает количества принятых/не принятых домашних работ у пользователя

        Args:
            _user_id(Int): ID пользователя
            _id_lessons_list(List): список ID уроков курса
            _id_course: ID курса

        Returns:
            count_accepted_homework(Int): количество принятых домашних работ
            count_no_accepted_homework(Int): количество не принятых домашних работ
        """

        homework_manager = HomeworkManager()

        if homework_manager.is_there_homework_in_sql_db():
            count_accepted_homework = homework_manager.get_count_accepted_homework_for_lessons_id(_user_id, _id_course)
            count_accepted_homework = 0 if len(count_accepted_homework) == 0 else count_accepted_homework[0][
                'sum_homework']

        else:
            id_lessons_set = homework_manager.get_id_lessons_list_with_completed_homework(_user_id)

            count_accepted_homework = len(id_lessons_set.intersection(_id_lessons_list))

        count_no_accepted_homework = len(_id_lessons_list) - count_accepted_homework

        return count_accepted_homework, count_no_accepted_homework

    def is_there_homework_in_sql(self) -> bool:
        """
        Проверяет, есть ли в PostgreSQL таблица с домашними работами

        Returns:
            True: есть
            False: нет
        """
        homework_manager = HomeworkManager()

        return homework_manager.is_there_homework_in_sql_db()
