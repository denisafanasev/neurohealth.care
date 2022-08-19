from models.action_manager import ActionManager
from models.homework_manager import HomeworkManager
from models.course_manager import EducationCourseManager
from models.module_manager import EducationModuleManager
from models.lesson_manager import EducationLessonManager
from models.room_chat_manager import RoomChatManager
from models.user_manager import UserManager
from models.message_manager import MessageManager


class HomeworkProfileService():
    """
    HomeworkProfileService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """
    def room_chat_entry(self, _id_room_chat, _id_user):
        """
        Подключает пользователя к чату

        Args:
            _id_room_chat(Int): ID чата

        Returns:
            RoomChat: чат
        """

        room_chat_manager = RoomChatManager()
        message_manager = MessageManager()

        room_chat = room_chat_manager.room_chat_entry(_id_room_chat)
        if room_chat is not None:
            room_chat.message = message_manager.get_messages(_id_room_chat, _id_user)

        return room_chat

    def add_message(self, _message, _id_lesson, _id_user):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
            _room_chat_id(Int): ID чата
            _user_id(Int): ID текущего пользователя
        """

        message_manager = MessageManager()
        room_chat_manager = RoomChatManager()

        if _message['id_room_chat'] is None:
            room_chat = room_chat_manager.get_room_chat(_id_user, _id_lesson)
            if room_chat is None:
                _message['id_room_chat'] = room_chat_manager.add_room_chat(_id_user, _id_lesson).id
            else:
                _message['id_room_chat'] = room_chat.id

        return message_manager.add_message(_message)


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

    def homework_answer_accepted(self, _id_homework, _user_id):
        """
        Меняет статус проверки домашней работы на "Принято"

        Args:
            _id_homework(Int): ID домашней работы
            _user_id(Int): ID текущего пользователя
        """

        homework_manager = HomeworkManager()
        action_manager = ActionManager()
        user_manager = UserManager()

        homework = homework_manager.homework_answer_accepted(_id_homework)
        user = user_manager.get_user_by_id(_user_id)
        lesson = self.get_lesson(homework.id_lesson)

        action_manager.add_notifications(homework.id_user, "принял", lesson.lessons.name, "homework_manager", user.login)

        return homework

    def homework_answer_no_accepted(self, _id_homework, _user_id):
        """
        Меняет статус проверки домашней работы на "Не принято"
        Args:
            _id_homework(Int): ID домашней работы
            _user_id(Int): ID текущего пользователя
        """

        homework_manager = HomeworkManager()
        action_manager = ActionManager()
        user_manager = UserManager()

        homework = homework_manager.homework_answer_no_accepted(_id_homework)
        user = user_manager.get_user_by_id(_user_id)
        lesson = self.get_lesson(homework.id_lesson)

        action_manager.add_notifications(homework.id_user, "не принял", lesson.lessons.name, "homework_manager", user.login)

        return homework

    def get_homework(self, _id_homework):
        """
        Возвращает данные домашней работы

        Args:
            _id_homework(Int): ID домашней работы

        Return:
            Homework: домашняя работа
        """
        homework_manager = HomeworkManager()
        lesson_manager = EducationLessonManager()

        homework = homework_manager.get_homework_by_id(_id_homework)
        homework.lesson = lesson_manager.get_lesson(homework.id_lesson)

        return homework

    def get_course(self, _id_course):
        """
        Возвращает данные курса
        Args:
            _id_course(Int): id курса
        Returns:
            Course: курс
        """

        course_manager = EducationCourseManager()

        return course_manager.get_course_by_id(_id_course)

    def get_lesson(self, _id_lesson):
        """
        Возвращает данные урок
        Args:
            _id_lesson(Int): id урока
        Returns:
            Lesson: урок
        """

        lesson_manager = EducationLessonManager()
        module_manager = EducationModuleManager()

        lesson = lesson_manager.get_lesson(_id_lesson)
        module = module_manager.get_module_by_id(lesson.id_module)
        module.lessons = lesson

        return module