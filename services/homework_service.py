from models.homework_manager import HomeworkManager
# from services.upload_service import UploadService
# from services.room_chat_service import RoomChatService
# from services import education_course_service
# from services import user_manager_service

class HomeworkService():

    def save_homework(self, _homework, _login_user, _id_room_chat):
        """
        Сохраняет данные домашнего задания
        Args:
            _homework(Dict): данные сданной домашней работы
            _id_room_chat(Int): индетификатор чата
            _login_user(String):
        """

        homework_manager = HomeworkManager()
        upload_service = UploadService()

        homework_files_list = upload_service.upload_files(_homework, _login_user)
        homework = homework_manager.create_homework(homework_files_list, _id_room_chat)

        homework_manager.create_homework_answer(homework.id)

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

        room_chat_service = RoomChatService()

        return room_chat_service.get_room_chat(_id_room_chat=_id_room_chat)

    def get_course(self, _id_course):
        """
        Возвращает данные курса
        Args:
            _id_course(Int): id курса
        Returns:
            Course: курс
        """

        course_service_service = education_course_service.EducationCourseService()

        return course_service_service.get_course_by_id(_id_course)

    def get_lesson(self, _id_lesson, _id_course):
        """
        Возвращает данные урок
        Args:
            _id_course(Int): id курса
            _id_lesson(Int): id урока
        Returns:
            Lesson: урок
        """

        course_service_service = education_course_service.EducationCourseService()

        return course_service_service.get_lesson(_id_lesson, _id_course, 1)

    # def get_education_stream(self, _id_education_stream):
    #
    #     stream_service = education_stream_service.EducationStreamService()
    #
    #     return stream_service.get_education_stream(_id_education_stream)

    def get_current_user(self, _login_user):
        """
        Возвращает данные текущего пользователя в системе
        Args:
            _login_user(String): логин пользователя
        Returns:
            User: пользователь
        """

        user_service = user_manager_service.UserManagerService()

        return user_service.get_current_user(_login_user)

    def change_homework_answer(self, _answer, _id_homework_answer):
        """
        Изменяет оценку домашнего задания
        Args:
            _answer(String): оценка
            _id_homework_answer(Int): индетификатор оценки домашего задания
        """

        homework_manager = HomeworkManager()

        homework_manager.change_homework_answer(_answer, _id_homework_answer)