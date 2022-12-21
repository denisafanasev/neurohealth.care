from datetime import datetime

import config
from models.action_manager import ActionManager
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

    def chenge_password(self, _user_id, _password, _password2, _current_password=''):
        """
        Обновляет в системе пароль пользователя

        Args:
            _user_id (Integer): ID пользователя
            _password (String): пароль пользователя
            _password2 (String): контрольный ввод пароля пользователя
            _current_password (String): текущий пароль пользователя. Defaults to ''

        Returns:
            String: ошибка при обновлении пароля пользователя
        """

        user_manager = UserManager()
        action_manager = ActionManager()

        error = user_manager.chenge_password(_user_id, _password, _password2, _current_password)
        login_superuser = user_manager.get_user_by_id(_user_id).login

        action_manager.add_notifications(login_superuser, "изменил", 'пароль', "user_manager", login_superuser)

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
        education_streams = []
        for education_stream in education_streams_list:
            if education_stream.status == 'идет':
                education_streams.append(education_stream)

        return education_streams

    def get_count_accepted_homeworks(self, _user_id, _id_course):
        """
        Возвращает количество сданных/не сданных домашних работ

        Args:
            _user_id(Int): ID
            _id_course(Int): ID

        Returns:
            count_accepted_homework(Int): количество сданных домашних работ
            count_no_accepted_homework(Int): количество не сданных домашних работ
        """
        module_manager = EducationModuleManager()
        lesson_manager = EducationLessonManager()
        homework_manager = HomeworkManager()

        module_list = module_manager.get_course_modules_list(_id_course)
        count_no_accepted_homework = 0
        count_accepted_homework = 0
        for module in module_list:
            lesson_list = lesson_manager.get_lessons_list_by_id_module(module.id)
            for lesson in lesson_list:
                if lesson.task:
                    is_accepted_homework = homework_manager.is_accepted_homework(_user_id, lesson.id)
                    if is_accepted_homework:
                        count_accepted_homework += 1
                    else:
                        count_no_accepted_homework += 1

        return count_accepted_homework, count_no_accepted_homework

