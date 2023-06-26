from models.action_manager import ActionManager
from models.homework_manager import HomeworkManager
from models.course_manager import EducationCourseManager
from models.module_manager import EducationModuleManager
from models.lesson_manager import EducationLessonManager
from models.homework_chat_manager import HomeworkChatManager
from models.user_manager import UserManager
from models.message_manager import MessageManager
from error import HomeworkCardServiceException


class HomeworkCardService():
    """
    HomeworkProfileService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """
    def homework_chat_entry(self, _id_homework_chat, _id_user):
        """
        Подключает пользователя к чату

        Args:
            _id_homework_chat(Integer): ID чата
            _id_user(Integer): ID пользователя

        Returns:
            HomeworkChat: чат
        """

        homework_chat_manager = HomeworkChatManager()
        message_manager = MessageManager()

        homework_chat = homework_chat_manager.homework_chat_entry(_id_homework_chat)
        if homework_chat is not None:
            homework_chat.message = message_manager.get_messages_for_superuser(_id_homework_chat, _id_user)

        return homework_chat

    def add_message(self, _message, _id_lesson, _id_user):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
            _id_lesson(Integer): ID урока
            _id_user(Integer): ID текущего пользователя

        Returns:
            Message: сообщение
        """

        message_manager = MessageManager()
        homework_chat_manager = HomeworkChatManager()

        homework_chat = homework_chat_manager.get_homework_chat(_id_user, _id_lesson)
        if homework_chat is None:
            _message['id_homework_chat'] = homework_chat_manager.add_homework_chat(_id_user, _id_lesson)
        else:
            _message['id_homework_chat'] = homework_chat.id

        return message_manager.add_message(_message)

    def get_user_by_id(self, _id_user):
        """
        Возвращает данные пользователя по ID

        Args:
            _id_user(Integer): ID пользователя

        Returns:
            User: пользователь
        """

        user_manager = UserManager()

        return user_manager.get_user_by_id(_id_user)

    def homework_answer_accepted(self, _id_homework, _user_id):
        """
        Меняет статус проверки домашней работы на "Принято"

        Args:
            _id_homework(Integer): ID домашней работы
            _user_id(Integer): ID текущего пользователя

        Return:
            Homework: домашняя работа
        """

        homework_manager = HomeworkManager()
        lesson_manager = EducationLessonManager()
        action_manager = ActionManager()
        user_manager = UserManager()

        homework = homework_manager.homework_answer_accepted(_id_homework)
        current_user = user_manager.get_user_by_id(_user_id)
        user = user_manager.get_user_by_id(homework.id_user)
        lesson = lesson_manager.get_lesson_by_id(homework.id_lesson)

        action_manager.add_notifications(user.login, "принял", lesson.name, "homework_manager", current_user)

        return homework

    def homework_answer_no_accepted(self, _id_homework, _user_id):
        """
        Меняет статус проверки домашней работы на "Не принято"

        Args:
            _id_homework(Integer): ID домашней работы
            _user_id(Integer): ID текущего пользователя

        Return:
            Homework: домашняя работа
        """

        homework_manager = HomeworkManager()
        lesson_manager = EducationLessonManager()
        action_manager = ActionManager()
        user_manager = UserManager()

        homework = homework_manager.homework_answer_no_accepted(_id_homework)
        current_user = user_manager.get_user_by_id(_user_id)
        user = user_manager.get_user_by_id(homework.id_user)
        lesson = lesson_manager.get_lesson_by_id(homework.id_lesson)

        action_manager.add_notifications(user.login, "не принял", lesson.name, "homework_manager", current_user)

        return homework

    def get_homework(self, _id_homework):
        """
        Возвращает данные домашней работы

        Args:
            _id_homework(Integer): ID домашней работы

        Return:
            Homework: домашняя работа
        """
        homework_manager = HomeworkManager()
        lesson_manager = EducationLessonManager()

        homework = homework_manager.get_homework_by_id(_id_homework)
        if homework is not None:
            homework.lesson = lesson_manager.get_lesson_by_id(homework.id_lesson)

            return homework

    def get_course(self, _id_course):
        """
        Возвращает данные курса

        Args:
            _id_course(Integer): id курса
        Returns:
            Course: курс
        """

        course_manager = EducationCourseManager()

        course = course_manager.get_course_by_id(_id_course)
        if course is None:
            raise HomeworkCardServiceException('Данный курс не найден.')

        return course

    def get_lesson(self, _id_lesson):
        """
        Возвращает данные урок
        
        Args:
            _id_lesson(Integer): id урока
        Returns:
            Lesson: урок
        """

        lesson_manager = EducationLessonManager()
        module_manager = EducationModuleManager()

        lesson = lesson_manager.get_lesson_by_id(_id_lesson)
        if lesson is None:
            raise HomeworkCardServiceException('Данный урок не найден.')
        module = module_manager.get_module_by_id(lesson.id_module)
        if lesson is None:
            raise HomeworkCardServiceException('Данный модуль не найден.')
        module.lessons = lesson

        return module

    def get_homework_chat(self, _id_lesson, _id_user, _id_current_user):
        """
        Возвращает данные чата по ID урока и пользователя

        Args:
            _id_lesson(Integer): ID урока
            _id_user(Integer): ID пользователя
            _id_current_user(Integer): ID текущего пользователя

        Returns:
            HomeworkChat: чат
        """
        homework_chat_manager = HomeworkChatManager()
        message_manager = MessageManager()

        homework_chat = homework_chat_manager.get_homework_chat(_id_user, _id_lesson)
        if homework_chat is not None:
            homework_chat.message = message_manager.get_messages_for_superuser(homework_chat.id, _id_user)

        return homework_chat
