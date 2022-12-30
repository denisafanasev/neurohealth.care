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

    def get_education_streams(self, _user_id):
        """
        Возвращает количество активных обучающих потоков, в которых текущий пользователь есть

        Args:
            _user_id(Int): ID текущего пользователя

        Returns:
            List(EducationStream): список обучающих потоков
        """
        education_stream_manager = EducationStreamManager()

        user = self.get_user_by_id(_user_id)
        if user.role == 'user':
            education_streams = education_stream_manager.get_education_streams_list_by_id_user(_user_id, user.role)
            education_streams_list = []
            for education_stream in education_streams:
                if education_stream.status == 'идет':
                    education_streams_list.append(education_stream)

            return education_streams_list

    def get_user_education_progress(self, _user_id, _id_course):
        """
        Возвращает количество сданных/не сданных модулей, а также количество сданных/не сданных домашних работ
        у текущего пользователя

        Args:
            _user_id(Int): ID

        Returns:
            data(Dict): словарь с количествами сданных/не сданных модулей и сданных/не сданных домашних работ
        """

        module_manager = EducationModuleManager()
        lesson_manager = EducationLessonManager()
        homework_manager = HomeworkManager()

        modules_list = module_manager.get_course_modules_list(_id_course)

        amount_modules_passed = 0
        amount_modules_no_passed = 0
        amount_homework_accepted = 0
        amount_homework_no_accepted = 0
        for module in modules_list:
            lessons_list = lesson_manager.get_lessons_list_by_id_module(module.id)
            is_passed = True
            for lesson in lessons_list:
                if lesson.task is not None:
                    homework_accepted = homework_manager.is_accepted_homework(_user_id, lesson.id)
                    if not homework_accepted:
                        is_passed = False
                        amount_homework_no_accepted += 1
                    else:
                        amount_homework_accepted += 1

            if is_passed:
                amount_modules_passed += 1
            else:
                amount_modules_no_passed += 1

        return amount_modules_passed, amount_modules_no_passed, amount_homework_accepted, amount_homework_no_accepted
