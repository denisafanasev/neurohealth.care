from models.course_manager import CourseManager
from services.action_service import ActionService
from services import user_manager_service
from services.homework_service import HomeworkService

class CourseService():
    """
    DownloadService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def get_course_modules_list(self, _id, _login_user):
        """
        Возвращает список модулей курса по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            modules_list(List): списко модулей курса
        """

        course_manager = CourseManager()

        modules_list = course_manager.get_course_modules_list(_id)
        #
        # if user.learning_stream_list != []:
        #     for id_learning_stream in user.learning_stream_list:
        #         learning_stream = learning_stream_service.get_learning_stream(id_learning_stream)
        #
        #         if learning_stream.course == _id and learning_stream.status == "идет":
        #             learning_stream.course = modules_list
        #             course = learning_stream
        #             break

        return modules_list


    def get_lesson(self, _id, _id_course, _id_video):
        """
        Возвращает данные урока

        Args:
            _id(Int): индентификатор урока
            _id_course(Int): индентификатор курса
            _id_video(Int): индентификатор видео

        Return:
            Lesson: класс Lesson, обернутый в класс Module
        """

        course_manager = CourseManager()
        action_service = ActionService()

        login_user = self.get_current_user('').login
        lesson = course_manager.get_lesson(_id, _id_course, _id_video)

        action_service.add_notifications(lesson, "view", '', "course_manager", login_user)

        return lesson

    def get_courses(self):
        """
        Возвращает список курсов

        Returns:
            courses(List): список курсов
        """

        course_manager = CourseManager()

        return course_manager.get_courses()

    def get_current_user(self, _id_course=None):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)

        Returns:
            User: пользователь
        """

        user_service = user_manager_service.UserManagerService()

        user = user_service.get_current_user('')
        if _id_course is not None:
            for learning_stream in user.learning_stream_list:
                if learning_stream.course == _id_course and learning_stream.status == "идет":
                    user.learning_stream_list = learning_stream

        return user

    def get_course_by_id(self, _id):
        """
        Возвращает курс по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            course(Course): курс
        """

        course_manager = CourseManager()

        return course_manager.get_course_by_id(_id)

    def get_user_list(self):

        user_service = user_manager_service.UserManagerService()

        return user_service.get_users()

    def save_homework(self, _files_list, _id_room_chat, ):

        homework_service = HomeworkService()

        login_user = self.get_current_user().login

        homework_service.save_homework(_files_list, login_user, _id_room_chat)