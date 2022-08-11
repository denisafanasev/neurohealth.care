from models.education_stream_manager import EducationStreamManager
from models.user_manager import UserManager
from models.course_manager import EducationCourseManager

class EducationStreamService():

    def get_education_streams_list(self):
        """
        Возвращает список обучающих потоков

        Returns:
            education_streams_list(List): список обучающих потоков
        """

        education_stream_manager = EducationStreamManager()
        course_manager = EducationCourseManager()

        education_streams = education_stream_manager.get_education_streams_list()
        education_streams_list = []

        for i_education_stream in education_streams:

            course = course_manager.get_course_by_id(i_education_stream.course)
            i_education_stream.course = course
            education_streams_list.append(i_education_stream)

        return education_streams_list

    def get_students_list(self, _id_user):
        """
        Возвращает список пользователей с ролью user

        Returns:
            students_list(List): список пользователей
        """

        user_manager = UserManager()

        users_list = user_manager.get_users(_id_user)
        students_list = []

        for user in users_list:
            if user.role == "user":
                students_list.append(user)

        return students_list

    def get_curators_list(self, _id_user):
        """
        Возвращает список пользователей с ролью superuser

        Returns:
            curators_list(List): список пользователей
        """

        user_manager = UserManager()

        users_list = user_manager.get_users(_id_user)
        curators_list = []

        for user in users_list:
            if user.role == "superuser":
                curators_list.append(user)

        return curators_list

    def get_courses_list(self, _id_user):
        """
        Возвращает список курсов

        Returns:
            (List): список курсов
        """

        course_service = EducationCourseManager()

        return course_service.get_courses()

    def get_education_stream(self, _id):
        """
        Возвращает обучающий поток по id

        Args:
            _id(Int): идентификатор обучающего потока
        """

        education_stream_manager = EducationStreamManager()
        course_manager = EducationCourseManager()

        education_stream = education_stream_manager.get_education_stream(_id)

        if education_stream is not None:
            education_stream.course = course_manager.get_course_by_id(education_stream.course)

        return education_stream

    def create_education_stream(self, _education_stream):
        """
        Создает обучающий поток

        Args:
            _education_stream(Dict): обучающий поток

        Returns:
            id(Int): идентификатор обучающего потока
        """
        education_stream_manager = EducationStreamManager()

        education_stream = education_stream_manager.create_education_stream(_education_stream)

        # user_service.add_user_in_education_stream(education_stream.id, education_stream.students_list)
        # user_service.add_user_in_education_stream(education_stream.id, education_stream.curators_list)

        return education_stream.id

    def change_education_stream(self, _education_stream, _old_students_list, _old_curators_list):
        """
        Изменяет данные обучающего потока

        Args:
            _education_stream(Dict): обучающий поток
            _old_students_list(List): предыдущий список студентов
            _old_curators_list(List): предыдющий список кураторов
        """

        education_stream_manager = EducationStreamManager()

        education_stream_manager.change_education_stream(_education_stream)

        # if education_stream.teacher not in education_stream.curators_list:
        #     education_stream.curators_list.append(education_stream.teacher)
        #
        # user_service.add_user_in_education_stream(education_stream.id, education_stream.curators_list)
        # user_service.add_user_in_education_stream(education_stream.id, education_stream.students_list)
        #
        # excluded_users_list = []
        # if _old_students_list != education_stream.students_list:
        #     excluded_users_list.extend([user for user in _old_students_list if user not in education_stream.students_list])
        #
        # if _old_curators_list != education_stream.curators_list:
        #     excluded_users_list.extend([user for user in _old_curators_list if user not in education_stream.curators_list])
        #
        # if excluded_users_list != []:
        #     user_service.exclusion_of_users_from_list(excluded_users_list, education_stream.id)

    def get_education_streams_list_by_login_user(self, _login_user, _role_user):

        education_stream_manager = EducationStreamManager()

        return education_stream_manager.get_education_streams_list_by_login_user(_login_user, _role_user)
