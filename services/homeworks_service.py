import os

import config
from models.homework_manager import HomeworkManager
from models.course_manager import EducationCourseManager
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

    def get_homeworks_list(self):
        """
        Возвращает список домашних работ пользователей

        Returns:
            List: список домашних работ
        """

        homework_manager = HomeworkManager()

        homework_list = homework_manager.get_homeworks()

        return homework_list

    def get_course(self, _id_lesson):
        """
        Возвращает данные курса

        Args:
            _id_lesson(Int): id урока

        Returns:
            Course: курс
        """

        course_manager = EducationCourseManager()
        module_manager = EducationModuleManager()
        lesson_manager = EducationLessonManager()

        lesson = lesson_manager.get_lesson_by_id(_id_lesson)
        module = module_manager.get_module_by_id(lesson.id_module)

        return course_manager.get_course_by_id(module.id_course)

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

    # def get_education_stream(self, _id_education_stream):
    #
    #     stream_service = education_stream_service.EducationStreamService()
    #
    #     return stream_service.get_education_stream(_id_education_stream)

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

        homework_chat = homework_chat_manager.get_homework_chat(_id_user, _id_lesson)
        if homework_chat is not None:
            homework_chat.unread_message_amount = message_manager.get_unread_messages_amount(homework_chat.id, _id_current_user)

        return homework_chat

    def get_courses_list(self):
        """
        Возвращает список основных курсов и их модули

        Returns:
            List: список курсов
        """
        course_manager = EducationCourseManager()
        module_manager = EducationModuleManager()
        lesson_manager = EducationLessonManager()

        courses_list = course_manager.get_courses()
        if courses_list is not None:
            courses = []
            for i_course in courses_list:
                # нужны только основные курсы, так как только по ним сдаются домашние работы
                if i_course.type == 'main':
                    modules_list = module_manager.get_course_modules_list(i_course.id)
                    if modules_list is not None:
                        modules = []
                        for i_module in modules_list:
                            i_module.lessons = lesson_manager.get_lessons_list_by_id_module(i_module.id)
                            modules.append(i_module)

                    i_course.modules = modules_list
                    courses.append(i_course)

            return courses

    def get_users_list_in_education_streams(self, _id_education_stream):
        """
        Возвращает список пользователей, которые находятся в обучающем потоке

        Returns:
            List: список пользователей
        """
        user_manager = UserManager()

        users_login_list = []
        with open(config.DATA_FOLDER + f'course_1/s{_id_education_stream}_users.txt') as f:
            users_login_list.extend(f.read().splitlines())

        # with open(config.DATA_FOLDER + 'course_1/s4_users.txt') as f:
        #     users_login_list.extend(f.read().splitlines())
        #
        # with open(config.DATA_FOLDER + 'course_1/s3_users.txt') as f:
        #     users_login_list.extend(f.read().splitlines())
        #
        # with open(config.DATA_FOLDER + 'course_1/s2_users.txt') as f:
        #     users_login_list.extend(f.read().splitlines())
        #
        # with open(config.DATA_FOLDER + 'course_1/s1_users.txt') as f:
        #     users_login_list.extend(f.read().splitlines())

        users_list = []
        for user_login in users_login_list:
            user = user_manager.get_user_by_login(user_login)
            if user is not None:
                users_list.append(user)

        return users_list

    def get_homeworks_list_by_id_user(self, _id_lesson, _id_user):
        """
        Возвращает список проверенных домашних работ по ID пользователя и урока

        Args:
            _id_lesson(Integer): ID урока
            _id_user(Integer): ID пользователя

        Returns:
            List: список домашних работ
        """
        homework_manager = HomeworkManager()

        homework_list = homework_manager.get_homeworks_list_by_id_lesson(_id_lesson, _id_user)
        if homework_list:
            return homework_list

    def get_homeworks_list_by_id_user_verified(self, _id_lesson, _id_user):
        """
        Возвращает список проверенных домашних работ по ID пользователя и урока

        Args:
            _id_lesson(Integer): ID урока
            _id_user(Integer): ID пользователя

        Returns:
            List: список домашних работ
        """
        homework_manager = HomeworkManager()

        homework_list = homework_manager.get_homeworks_list_by_id_lesson(_id_lesson, _id_user)
        if homework_list:
            homeworks = [homework for homework in homework_list if homework.status is not None]
            return homeworks

    def get_homeworks_list_by_id_user_no_verified(self, _id_lesson, _id_user):
        """
        Возвращает список не проверенных домашних работ по ID пользователя и урока

        Args:
            _id_lesson(Integer): ID урока
            _id_user(Integer): ID пользователя

        Returns:
            List: список домашних работ
        """
        homework_manager = HomeworkManager()

        homework_list = homework_manager.get_homeworks_list_by_id_lesson_no_verified(_id_lesson, _id_user)
        if homework_list:
            return homework_list

    def get_lessons(self):
        """
        Возвращает данные всех уроков, которые есть в базе данных

        Return:
            List(Lesson): список уроков
        """
        lesson_manager = EducationLessonManager()

        return lesson_manager.get_lessons()

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