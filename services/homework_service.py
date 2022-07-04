from models.homework_manager import HomeworkManager
from models.room_chat_manager import RoomChatManager
from models.course_manager import EducationCourseManager
from models.education_stream_manager import EducationStreamManager
from models.user_manager import UserManager


class HomeworkService():

    def get_homeworks_list(self):
        """
        Возвращает список домашних работ пользователей
        Returns:
            List: список домашних работ
        """

        homework_manager = HomeworkManager()

        homework_list = homework_manager.get_homeworks()

        return homework_list

    def get_room_chat(self, _id_room_chat):
        """
        Возвращает данные комнаты чата
        Args:
            _id_room_chat(Int): id чата
        Returns:
            RoomChat: чат
        """

        room_chat_manager = RoomChatManager()

        room_chat = room_chat_manager.get_room_chat(_id_room_chat=_id_room_chat)
        name_room_chat = room_chat.name.split("_")
        id_dict = {"course": int(name_room_chat[1]), "lesson": int(name_room_chat[2]), "user": name_room_chat[3]}

        return room_chat, id_dict

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

        course_manager = EducationCourseManager()

        return course_manager.get_lesson(_id_lesson, _id_course, 1)

    # def get_education_stream(self, _id_education_stream):
    #
    #     stream_service = education_stream_service.EducationStreamService()
    #
    #     return stream_service.get_education_stream(_id_education_stream)

    def get_user(self, _user):
        """
        Возвращает данные текущего пользователя в системе
        Args:
            _user(String): логин пользователя
        Returns:
            User: пользователь
        """

        user_manager = UserManager()

        if _user.isdigit():
            return user_manager.get_user_by_id(int(_user))
        else:
            return user_manager.get_user_by_login(_user)

    def change_homework_answer(self, _answer, _id_homework_answer):
        """
        Изменяет оценку домашнего задания
        Args:
            _answer(String): оценка
            _id_homework_answer(Int): индетификатор оценки домашего задания
        """

        homework_manager = HomeworkManager()

        homework_manager.change_homework_answer(_answer, _id_homework_answer)

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

    def get_homework_by_id(self, _id_homework):

        homework_manager = HomeworkManager()

        return homework_manager.get_homework_by_id(_id_homework)