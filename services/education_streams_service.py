from models.education_stream_manager import EducationStreamManager
from models.user_manager import UserManager
from models.course_manager import EducationCourseManager


class EducationStreamsService():
    """
    Класс сервиса списка обучающих потоков
    """
    def get_education_streams(self):
        """
        Возвращает список обучающих потоков

        Returns:
            education_streams_list(List): список обучающих потоков
        """

        education_stream_manager = EducationStreamManager()
        course_manager = EducationCourseManager()

        education_streams = education_stream_manager.get_education_streams()
        education_streams_list = []

        for i_education_stream in education_streams:

            course = course_manager.get_course_by_id(i_education_stream.course)
            i_education_stream.course = course
            education_streams_list.append(i_education_stream)

        return education_streams_list

    def get_user_by_id(self, _user_id):
        """
        Возвращает пользователя по ID

        Args:
            _user_id(Int): ID пользователя

        Returns:
            User: пользователь
        """

        user_manager = UserManager()

        return user_manager.get_user_by_id(_user_id)
