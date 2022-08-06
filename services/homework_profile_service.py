from models.action_manager import ActionManager
from models.homework_manager import HomeworkManager
from models.course_manager import EducationCourseManager
from models.lesson_manager import EducationLessonManager
from models.room_chat_manager import RoomChatManager
from models.user_manager import UserManager


class HomeworkProfileService():


    def room_chat_entry(self, _id_lesson, _id_course, _id_user, _id_room_chat, _id_education_stream, _id_module):
        """
        Подключает пользователя к чату

        Args:
            _id_lesson(Int): индентификатор урока
            _id_user(User): ID пользователя
            _id_course(Int): индентификатор курса
            _id_room_chat(Int): индентификатор чата

        Returns:
            RoomChat: чат
        """

        room_chat_manager = RoomChatManager()
        user_manager = UserManager()

        user = user_manager.get_user_by_id(_id_user)

        return room_chat_manager.room_chat_entry(_id_lesson, user, _id_course, _id_room_chat, _id_education_stream,
                                                 _id_module)

    def add_message(self, _message, _room_chat_id, _user_id):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
            _room_chat_id(Int): индентификатор чата
        """

        room_chat_manager = RoomChatManager()
        user_manager = UserManager()

        _message["name_sender"] = user_manager.get_user_by_id(_user_id).login

        return room_chat_manager.add_message(_message, _room_chat_id)


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

    def change_homework_answer(self, _answer, _id_homework_answer, _user_id):
        """
        Изменяет оценку домашнего задания
        Args:
            _answer(String): оценка
            _id_homework_answer(Int): ID оценки домашего задания
            _user_id(Int): ID текущего пользователя
        """

        homework_manager = HomeworkManager()
        action_manager = ActionManager()
        user_manager = UserManager()

        homework_answer = homework_manager.change_homework_answer(_answer, _id_homework_answer)
        homework = homework_manager.get_homework_by_id(homework_answer.id_homework)
        user = user_manager.get_user_by_id(_user_id)
        if homework.id_user is None:
            homework = self.update_homework(homework)
        lesson = self.get_lesson(homework.id_lesson, homework.id_course)
        if homework_answer.answer:
            action = "принял"
        else:
            action = "не принял"

        action_manager.add_notifications(homework.id_user, action, lesson.lessons.name, "homework_manager", user.login)

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
        if homework.id_user is None:
            homework = self.update_homework(homework)

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

    def get_lesson(self, _id_lesson, _id_course):
        """
        Возвращает данные урок
        Args:
            _id_course(Int): id курса
            _id_lesson(Int): id урока
        Returns:
            Lesson: урок
        """

        lesson_manager = EducationLessonManager()

        return lesson_manager.get_lesson(_id_lesson)