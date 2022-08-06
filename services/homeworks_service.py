from models.homework_manager import HomeworkManager
from models.room_chat_manager import RoomChatManager
from models.course_manager import EducationCourseManager
from models.lesson_manager import EducationLessonManager
from models.education_stream_manager import EducationStreamManager
from models.user_manager import UserManager
from models.action_manager import ActionManager


class HomeworksService():

    def get_homeworks_list(self):
        """
        Возвращает список домашних работ пользователей
        Returns:
            List: список домашних работ
        """

        homework_manager = HomeworkManager()

        homework_list = homework_manager.get_homeworks()

        return homework_list

    def update_homework(self, _homework):
        """
        Возвращает данные комнаты чата
        Args:
            _homework(Homework): домашняя работа
        Returns:
            RoomChat: чат
        """

        room_chat_manager = RoomChatManager()
        user_manager = UserManager()
        homework_manager = HomeworkManager()

        room_chat = room_chat_manager.get_room_chat(_id_room_chat=_homework.id_room_chat)
        name_room_chat = room_chat.name.split("_")
        id_dict = {"course": int(name_room_chat[1]), "lesson": int(name_room_chat[2]), "user": name_room_chat[3]}
        if len(name_room_chat) > 4:
            for i in range(0, len(name_room_chat) - 3):
                if i + 4 < len(name_room_chat):
                    id_dict['user'] = "_".join([id_dict['user'], name_room_chat[i + 4]])
                else:
                    break

        _homework.id_course = id_dict['course']
        _homework.id_lesson = id_dict['lesson']
        _homework.id_user = user_manager.get_user_by_login(id_dict['user']).user_id
        homework_manager.update_homework(_homework)

        return _homework

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

