from models.course_manager import EducationCourseManager
from models.education_stream_manager import EducationStreamManager
from models.homework_manager import HomeworkManager
from models.lesson_manager import EducationLessonManager
from models.module_manager import EducationModuleManager
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

    def get_modules_passed(self, _user_id):
        """
        Возвращает количество сданных/не сданных модулей, а также количество сданных/не сданных домашних работ
        у текущего пользователя

        Args:
            _user_id(Int): ID

        Returns:
            data(Dict): словарь с количествами сданных/не сданных модулей и сданных/не сданных домашних работ
        """
        course_manager = EducationCourseManager()
        module_manager = EducationModuleManager()
        lesson_manager = EducationLessonManager()
        homework_manager = HomeworkManager()

        courses_list = course_manager.get_courses()
        modules_list = []
        for course in courses_list:
            if course.type == "main":
                modules_list = module_manager.get_course_modules_list(course.id)

        data = {
            'count_modules_passed': 0,
            'count_modules_no_passed': 0,
            'count_homework_accepted': 0,
            'count_homework_no_accepted': 0
        }
        for module in modules_list:
            lessons_list = lesson_manager.get_lessons_list_by_id_module(module.id)
            is_passed = True
            for lesson in lessons_list:
                homework_accepted = homework_manager.is_accepted_homework(_user_id, lesson.id)
                if not homework_accepted:
                    is_passed = False
                    data['count_homework_no_accepted'] += 1
                else:
                    data['count_homework_accepted'] += 1

            if is_passed:
                data['count_modules_passed'] += 1
            else:
                data['count_modules_no_passed'] += 1

        return data
