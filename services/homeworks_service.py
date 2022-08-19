from models.homework_manager import HomeworkManager
from models.course_manager import EducationCourseManager
from models.module_manager import EducationModuleManager
from models.lesson_manager import EducationLessonManager
from models.education_stream_manager import EducationStreamManager
from models.user_manager import UserManager
from models.room_chat_manager import RoomChatManager
from models.message_manager import MessageManager


class HomeworksService():
    """
    HomeworksService - класс бизнес-логики сервиса управления настройками приложения
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
            _id_course(Int): id курса
        Returns:
            Course: курс
        """

        course_manager = EducationCourseManager()
        module_manager = EducationModuleManager()
        lesson_manager = EducationLessonManager()

        lesson = lesson_manager.get_lesson(_id_lesson)
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

        lesson = lesson_manager.get_lesson(_id_lesson)
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

    def get_room_chat(self, _id_lesson, _id_user, _id_current_user):
        """
        Возвращает данные комнаты чата

        Args:
            _id_lesson(Integer): ID урока
            _id_user(Integer): ID пользователя

        Returns:
            RoomChat: комната чата
        """

        room_chat_manager = RoomChatManager()
        message_manager = MessageManager()

        room_chat = room_chat_manager.get_room_chat(_id_user, _id_lesson)
        if room_chat is not None:
            room_chat.unread_message_amount = message_manager.get_unread_messages_amount(room_chat.id, _id_current_user)

            return room_chat