from models.learning_stream_manager import LearningStreamManager
from services.course_service import CourseService
from services import user_manager_service

class LearningStreamService():

    def get_learning_streams_list(self):
        """
        Возвращает список обучающих потоков

        Returns:
            learning_streams_list(List): список обучающих потоков
        """

        learning_stream_manager = LearningStreamManager()
        course_service = CourseService()

        learning_streams = learning_stream_manager.get_learning_streams_list()
        learning_streams_list = []

        for i_learning_stream in learning_streams:

            course = course_service.get_course_by_id(i_learning_stream.course)
            i_learning_stream.course = course
            learning_streams_list.append(i_learning_stream)

        return learning_streams_list

    def get_students_list(self):
        """
        Возвращает список пользователей с ролью user

        Returns:
            students_list(List): список пользователей
        """

        user_service = user_manager_service.UserManagerService()

        users_list = user_service.get_users()
        students_list = []

        for user in users_list:
            if user.role == "user":
                students_list.append(user)

        return students_list

    def get_curators_list(self):
        """
        Возвращает список пользователей с ролью superuser

        Returns:
            curators_list(List): список пользователей
        """

        user_service = user_manager_service.UserManagerService()

        users_list = user_service.get_users()
        curators_list = []

        for user in users_list:
            if user.role == "superuser":
                curators_list.append(user)

        return curators_list

    def get_courses_list(self):
        """
        Возвращает список курсов

        Returns:
            (List): список курсов
        """

        course_service = CourseService()

        return course_service.get_courses()

    def get_learning_stream(self, _id):
        """
        Возвращает обучающий поток по id

        Args:
            _id(Int): идентификатор обучающего потока
        """

        learning_stream_manager = LearningStreamManager()
        course_service = CourseService()

        learning_stream = learning_stream_manager.get_learning_stream(_id)

        if learning_stream is not None:
            learning_stream.course = course_service.get_course_by_id(learning_stream.course)

        return learning_stream

    def create_learning_stream(self, _learning_stream):
        """
        Создает обучающий поток

        Args:
            _learning_stream(Dict): обучающий поток

        Returns:
            id(Int): идентификатор обучающего потока
        """
        learning_stream_manager = LearningStreamManager()

        learning_stream = learning_stream_manager.create_learning_stream(_learning_stream)

        # user_service.add_user_in_learning_stream(learning_stream.id, learning_stream.students_list)
        # user_service.add_user_in_learning_stream(learning_stream.id, learning_stream.curators_list)

        return learning_stream.id

    def change_learning_stream(self, _learning_stream, _old_students_list, _old_curators_list):
        """
        Изменяет данные обучающего потока

        Args:
            _learning_stream(Dict): обучающий поток
            _old_students_list(List): предыдущий список студентов
            _old_curators_list(List): предыдющий список кураторов
        """

        learning_stream_manager = LearningStreamManager()

        learning_stream_manager.change_learning_stream(_learning_stream)

        # if learning_stream.teacher not in learning_stream.curators_list:
        #     learning_stream.curators_list.append(learning_stream.teacher)
        #
        # user_service.add_user_in_learning_stream(learning_stream.id, learning_stream.curators_list)
        # user_service.add_user_in_learning_stream(learning_stream.id, learning_stream.students_list)
        #
        # excluded_users_list = []
        # if _old_students_list != learning_stream.students_list:
        #     excluded_users_list.extend([user for user in _old_students_list if user not in learning_stream.students_list])
        #
        # if _old_curators_list != learning_stream.curators_list:
        #     excluded_users_list.extend([user for user in _old_curators_list if user not in learning_stream.curators_list])
        #
        # if excluded_users_list != []:
        #     user_service.exclusion_of_users_from_list(excluded_users_list, learning_stream.id)

    def get_learning_streams_list_by_login_user(self, _login_user, _role_user):

        learning_stream_manager = LearningStreamManager()

        return learning_stream_manager.get_learning_streams_list_by_login_user(_login_user, _role_user)
