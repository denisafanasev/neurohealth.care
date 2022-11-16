import os
from datetime import datetime

import config
from models.action_manager import ActionManager
from models.course_manager import EducationCourseManager
from models.homework_manager import HomeworkManager
from models.homework_chat_manager import HomeworkChatManager
from models.upload_manager import UploadManager
from models.user_manager import UserManager
from models.users_file_manager import UsersFileManager
from models.module_manager import EducationModuleManager
from models.lesson_manager import EducationLessonManager
from models.message_manager import MessageManager

from error import HomeworkManagerException, EducationCourseLessonServiceException


class EducationCourseLessonService():
    """
    EducationCourseLessonService - класс бизнес-логики сервиса управления настройками приложения.
    Возвращает в слой отображения объекты в доменной модели.
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def get_lesson(self, _user_id, _lesson_id, _id_video):
        """
        Возвращает данные урока

        Args:
            _lesson_id(Int): ID урока
            _id_video(Int): ID видео
            _user_id(Int): ID текущего пользователя в системе

        Return:
            Lesson: класс Lesson, обернутый в класс Module
        """
        module_manager = EducationModuleManager()
        lesson_manager = EducationLessonManager()

        lesson = lesson_manager.get_lesson_by_id(_lesson_id, _id_video)
        if lesson is not None:
            module = module_manager.get_module_by_id(lesson.id_module)
            module.lessons = lesson

            return module

    def homework_chat_entry(self, _id_homework_chat, _id_user):
        """
        Подключает пользователя к чату

        Args:
            _id_homework_chat(Integer): ID комнаты чата
            _id_user(Integer): ID текущего пользователя
        Returns:
            HomeworkChat: чат
        """

        homework_chat_manager = HomeworkChatManager()
        message_manager = MessageManager()

        homework_chat = homework_chat_manager.homework_chat_entry(int(_id_homework_chat))
        if homework_chat is not None:
            homework_chat.message = message_manager.get_messages(homework_chat.id, _id_user)

        return homework_chat

    def add_message(self, _message, _id_lesson):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): текст сообщения
            _id_lesson(Integer): ID урока

        Return:
            Message: сообщение
        """

        message_manager = MessageManager()
        homework_chat_manager = HomeworkChatManager()
        user_manager = UserManager()
        lesson_manager = EducationLessonManager()

        # проверка на наличие в базе данных пользователя и урока
        user = user_manager.get_user_by_id(_message['id_user'])
        if user is None:
            raise EducationCourseLessonServiceException('Не удалось сохранить сообщение.')

        lesson = lesson_manager.get_lesson_by_id(_id_lesson)
        if lesson is None:
            raise EducationCourseLessonServiceException('Не удалось сохранить сообщение.')

        homework_chat = homework_chat_manager.get_homework_chat(_message['id_user'], _id_lesson)
        if homework_chat is None:
            _message['id_homework_chat'] = homework_chat_manager.add_homework_chat(_message['id_user'], _id_lesson)
        else:
            _message['id_homework_chat'] = homework_chat.id

        message_manager.add_message(_message)

    def get_user_by_id(self, _user_id):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)

        Returns:
            User: пользователь
        """

        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)

        return user

    def get_course_by_id(self, _id):
        """
        Возвращает курс по id

        Args:
            _id(Integer): индентификатор курса

        Returns:
            Course: курс
        """

        course_manager = EducationCourseManager()

        return course_manager.get_course_by_id(_id)

    def save_homework(self, _files_list, _current_user_id, _text, _id_lesson):
        """
        Сохраняет домашнюю работу
        Args:
            _files_list(Dict): данные сданной домашней работы
            _text(String): ответ на задание
            _current_user_id(Integer): ID пользователя
            _id_lesson(Integer): ID урока

        Return:
            Homework: домашняя работа
        """

        homework_manager = HomeworkManager()
        user_manager = UserManager()
        upload_service = UploadManager()
        action_manager = ActionManager()
        lesson_manager = EducationLessonManager()

        # проверка на наличие в базе данных пользователя и урока
        user = user_manager.get_user_by_id(_current_user_id)
        if user is None:
            raise HomeworkManagerException('Не удалось сохранить домашнюю работу.')

        lesson = lesson_manager.get_lesson_by_id(_id_lesson)
        if lesson is None:
            raise HomeworkManagerException('Не удалось сохранить домашнюю работу.')

        homework_files_list = upload_service.upload_files(_files_list, user.login)
        homework_manager.create_homework(homework_files_list, _text, _current_user_id, _id_lesson)

        action_manager.add_notifications("", "сдал", lesson.name, "homework_manager", user.login)

    def get_last_homework(self, _id_lesson, _user_id):
        """
        Возвращает последнюю сданную домашнюю работу по ID чата.
        Дата сдачи возвращается первой сданной домашней работы.
        Args:
            _id_lesson(Integer): ID урока
            _user_id(Integer): ID пользователя

        Return:
            Homework: домашняя работа
        """
        homework_manager = HomeworkManager()
        users_file_manager = UsersFileManager()

        homework_list = homework_manager.get_homeworks_list_by_id_lesson(_id_lesson, _user_id)
        date = datetime.strptime("01/01/2000", "%d/%m/%Y")
        date_first_homework = datetime.now()
        last_homework = None
        if homework_list is not None:
            # находим последнюю домашнюю работу, сданной пользователем, по уроку
            for homework in homework_list:
                if homework.date_delivery >= date:
                    date = homework.date_delivery
                    last_homework = homework

            # находим дату сдачи первой домашней работы, сданной пользователем, по уроку
            for homework in homework_list:
                if homework.date_delivery <= date_first_homework:
                    date_first_homework = homework.date_delivery

            # записываем список файлов в домашней работе вместе с их размером
            files = users_file_manager.get_size_files(last_homework.users_files_list)
            last_homework.users_files_list = files
            last_homework.date_delivery = date_first_homework

            return last_homework

    def get_neighboring_lessons(self, _id_lesson, _id_course, _user_id):
        """
        Возвращает данные соседних уроков текущего урока

        Args:
            _user_id(Int): ID текущего пользователя
            _id_lesson(Int): ID текущего урока
            _id_course(Int): ID текущего курса

        Returns:
            Dict: данные соседних уроков текущего урока
        """

        lesson_manager = EducationLessonManager()
        module_manager = EducationModuleManager()

        neighboring_lessons = lesson_manager.get_neighboring_lessons(_id_lesson)
        # если уроки найдены, то оборачиваем их в класс Module
        if neighboring_lessons['next_lesson'] is not None:
            module = module_manager.get_module_by_id(neighboring_lessons['next_lesson'].id_module)
            module.lessons = neighboring_lessons['next_lesson']
            neighboring_lessons['next_lesson'] = module

        if neighboring_lessons['previous_lesson'] is not None:
            module = module_manager.get_module_by_id(neighboring_lessons['previous_lesson'].id_module)
            module.lessons = neighboring_lessons['previous_lesson']
            neighboring_lessons['previous_lesson'] = module

        return neighboring_lessons

    def is_course_module_avalable_for_user(self, _course_id, _module_id, _user_id):
        """
        Функция проверки доступности модуля для пользователя

        Args:
            _course_id (Integer): ID курса
            _module_id (Integer): ID модуля
            _user_id (Integer): ID пользователя

        Returns:
            Boolean: доступен модуль для пользователя или нет
        """
        course_manager = EducationCourseManager()
        module_manager = EducationModuleManager()
        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)

        # если пользователь суперпользователь, то сразу возвращаем True и больше ничего не проверяем
        if user.role == 'superuser':
            return True

        # если это обычный пользователь, посмотрим что за курс и модуль
        course = course_manager.get_course_by_id(_course_id)
        course_modules = module_manager.get_course_modules_list(_course_id)
        first_module = course_modules[0]

        if course.type == 'additional':
            # если дополнительный курс, то проверяем доступность модуля для пользователя по налицию у него общей подписки
            if user.education_module_expiration_date >= datetime.now():
                return True
            elif first_module.id == _module_id:
                return True
            else:
                return False
        else:
            # если это основной курс, то проверяем доступность модуля по наличию подписки на обучающий курс

            # TODO: это надо перенести в целевую модель проверки вхождения пользователя в обущающий поток

            # проверяем, есть ли пользователь в списках участников пятого потока
            for i in range(1, min(len(course_modules) + 1, 5)):
                if course_modules[i - 1].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s5_users.txt') as f:
                        course_users_list = f.read().splitlines()

                    for course_user in course_users_list:
                        if course_user.lower() == user.login:
                            return True

            # проверяем, есть ли пользователь в списках участников четвертого потока
            for i in range(1, min(len(course_modules) + 1, 9)):
                if course_modules[i - 1].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s4_users.txt') as f:
                        course_users_list = f.read().splitlines()

                    for course_user in course_users_list:
                        if course_user.lower() == user.login:
                            return True

            # проверяем, есть ли пользователь в списках участников третьего потока
            for i in range(1, min(len(course_modules) + 1, 9)):
                if course_modules[i - 1].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s3_users.txt') as f:
                        course_users_list = f.read().splitlines()

                    for course_user in course_users_list:
                        if course_user.lower() == user.login:
                            return True

            # # проверяем, есть ли пользователь в списках участников второго потока
            # for i in range(1, min(len(course_modules) + 1, 9)):
            #     if course_modules[i - 1].id == _module_id:
            #         with open(config.DATA_FOLDER + 'course_1/s2_users.txt') as f:
            #             course_users_list = f.read().splitlines()
            #
            #         for course_user in course_users_list:
            #             if course_user.split()[0].lower() == user.login:
            #                 return True

            return False

    def get_homework_chat(self, _id_lesson, _id_user):
        """
        Возвращает данные чата

        Args:
            _id_lesson(Integer): ID урока
            _id_user(Integer): ID пользователя

        Return:
            HomeworkChat: чат
        """
        homework_chat_manager = HomeworkChatManager()
        message_manager = MessageManager()

        homework_chat = homework_chat_manager.get_homework_chat(_id_user, _id_lesson)
        if homework_chat is not None:
            homework_chat.message = message_manager.get_messages(homework_chat.id, _id_user)

        return homework_chat