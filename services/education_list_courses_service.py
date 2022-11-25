from models.course_manager import EducationCourseManager
from models.education_stream_manager import EducationStreamManager
from models.user_manager import UserManager


class EducationListCoursesService():
    """
    EducationCourseLessonService - класс бизнес-логики сервиса управления настройками приложения.
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """
    def get_courses(self):
        """
        Возвращает список курсов

        Returns:
            courses(List): список курсов
        """

        course_manager = EducationCourseManager()

        return course_manager.get_courses()

    def get_user_by_id_and_course_id(self, _user_id, _course_id):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)
            _id_course - Required  : id курса (Int)

        Returns:
            User: пользователь
        """

        user_manager = UserManager()
        education_stream_manager = EducationStreamManager()

        user = user_manager.get_user_by_id(_user_id)

        if _course_id is not None:
            education_stream = education_stream_manager.get_education_stream_by_id_user_and_id_course(_user_id,
                                                                                                      _course_id)
            if education_stream.status == "идет":
                user.education_stream_list = education_stream

        return user

    def get_user_by_id(self, _user_id):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)

        Returns:
            User: пользователь
        """

        user_manager = UserManager()
        user = user_manager.get_user_by_id(_user_id)

        return user