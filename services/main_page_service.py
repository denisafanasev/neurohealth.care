from datetime import datetime

import config
from models.action_manager import ActionManager
from models.course_manager import EducationCourseManager
from models.homework_manager import HomeworkManager
from models.lesson_manager import EducationLessonManager
from models.module_manager import EducationModuleManager
from models.user_manager import UserManager
from models.education_stream_manager import EducationStreamManager
class MainPageService():
    """
    MainPageService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """
    
    def init(self):
        pass

    def get_data(self):
        return "Data"

    def get_user_by_id(self, _user_id):
        """
        Фукция возвращает пользователя по его id

        Args:
            _user_id (_type_): id пользователя

        Returns:
            User: пользователь
        """        

        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)

        return user

    def chenge_password(self, _user_id, _password, _password2, _current_password):
        """
        Обновляет в системе пароль пользователя

        Args:
            _user_id (Integer): ID пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _current_password (String): текущий пароль пользователя

        Returns:
            String: ошибка при обновлении пароля пользователя
        """

        user_manager = UserManager()
        action_manager = ActionManager()

        error = user_manager.chenge_password(_user_id, _password, _password2, _current_password)
        user = user_manager.get_user_by_id(_user_id)

        action_manager.add_notifications(user.login, "изменил", 'пароль', "user_manager", user)

        return error

    def get_actions(self, _user_id):
        """
        Возвращает список действий, сделанных авторизованным пользователем(если авторизованный пользователь админ,
        то возвращает список действий всех пользователей, которые есть в системе)

        Args:
            _user_id(Integer): ID текущего пользователя

        Returns:
            actions(List): список испытуемых
        """

        action_manager = ActionManager()
        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)

        return action_manager.get_last_ten_actions(user)

    def get_education_streams(self, _user_id):
        """
        Возвращает список курсов, которые доступны пользователю

        Args:
            _user_id(Int): ID пользователя

        Returns:
            List(Course): список доступных пользователю курсов
        """
        education_stream_manager = EducationStreamManager()

        user = self.get_user_by_id(_user_id)
        education_streams_list = education_stream_manager.get_education_streams_list_by_id_user(user.user_id, user.role)
        if user.role == 'superuser':
            education_streams_list.extend(education_stream_manager.get_education_streams_by_teacher(user.user_id))

        education_streams = []
        for education_stream in education_streams_list:
            if education_stream.status == 'идет':
                education_streams.append(education_stream)

        return education_streams

    def get_progress_users(self, _id_course, _id_accepted_lessons_list):
        """
        Возвращает прогресс текущего пользователя
        Args:
            _id_course(Int): ID
            _id_accepted_lessons_list
        Returns
        """

        course_manager = EducationCourseManager()
        module_manager = EducationModuleManager()
        lesson_manager = EducationLessonManager()

        course = course_manager.get_course_by_id(_id_course)

        modules_list = module_manager.get_course_modules_list(course.id)
        lessons_list = []
        for module in modules_list:
            lessons_list.extend(lesson_manager.get_lessons_list_by_id_module(module.id))

        id_lessons_list = set(lesson.id for lesson in lessons_list if lesson.task is not None)
        count_accepted_homework = len(id_lessons_list.intersection(_id_accepted_lessons_list))
        count_no_accepted_homework = len(id_lessons_list) - count_accepted_homework

        return course.name, count_accepted_homework, count_no_accepted_homework

    def get_id_lessons_list_with_completed_homework(self, _user_id):
        """
        Возвращает множество из ID уроков, по которым домашние работы текущего пользователя приняты
        Args:
            _user_id(Int): ID текущего пользователя

        Returns:
            List: список из ID уроков
        """
        homework_manager = HomeworkManager()

        return homework_manager.get_id_lessons_list_with_completed_homework(_user_id)

