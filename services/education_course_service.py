#TODO: передалать на использование менеджера и не сервиса
from services.action_service import ActionService
from models.user_manager import UserManager
from models.course_manager import EducationCourseManager
from models.education_stream_manager import EducationStreamManager

from datetime import datetime
import config

class EducationCourseService():
    """
    DownloadService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def get_course_modules_list(self, _id, _user_id):
        """
        Возвращает список модулей курса по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            modules_list(List): списко модулей курса
        """

        course_manager = EducationCourseManager()

        modules_list = course_manager.get_course_modules_list(_id)
        #
        # if user.education_stream_list != []:
        #     for id_education_stream in user.education_stream_list:
        #         education_stream = education_stream_service.get_education_stream(id_education_stream)
        #
        #         if education_stream.course == _id and education_stream.status == "идет":
        #             education_stream.course = modules_list
        #             course = education_stream
        #             break

        return modules_list


    def get_lesson(self, _user_id, _lesson_id, _id_course, _id_video):
        """
        Возвращает данные урока

        Args:
            _lesson_id(Int): индентификатор урока
            _id_course(Int): индентификатор курса
            _id_video(Int): индентификатор видео

        Return:
            Lesson: класс Lesson, обернутый в класс Module
        """

        course_manager = EducationCourseManager()
        user_manager = UserManager()
        action_service = ActionService()

        login_user = user_manager.get_user_by_id(_user_id).login
        lesson = course_manager.get_lesson(_lesson_id, _id_course, _id_video)

        action_service.add_notifications(lesson, "view", '', "course_manager", login_user)

        return lesson
    
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

        education_streams = education_stream_manager.get_education_streams_list_by_login_user(user.login, user.role)

        if _course_id is not None:
            for education_stream in education_streams:
                if education_stream.course == _course_id and education_stream.status == "идет":
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

    def get_course_by_id(self, _id):
        """
        Возвращает курс по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            course(Course): курс
        """

        course_manager = EducationCourseManager()

        return course_manager.get_course_by_id(_id)
    
    def is_course_module_avalable_for_user(self, _course_id, _module_id, _user_id):
        """
        Функция проверки доступности модуля для пользователя

        Args:
            _course_id (Integer): ID курса
            _module_id (Integer): ID модуля
            _user_id (Integer): ID пользователя

        Returns:
            Boolean: доступен модуль для пользователя или нет
        """        
        course_manager = EducationCourseManager()
        user_manager = UserManager()

        user = user_manager.get_user_by_id(_user_id)
        
        # если пользователь суперпользователь, то сразу возвращаем True и больше ничего не проверяем
        if user.role == 'superuser':
            return True

        # если это обычный пользователь, по смотрим что за курс и модуль
        course = course_manager.get_course_by_id(_course_id)

        if course.type == 'additional':
            # если дополнительный курс, то проверяем доступность модуля для пользователя по налицию у него общей подписки
            if user.education_module_expiration_date >= datetime.now():
                return True
            else:
                return False
        else:
            # если это основной курс, то проверяем доступность модуля по наличию подписки на обучающий курс

            # TODO: это надо перенести в целевую модель проверки вхождения пользователя в обущающий поток   

            course_modules = course_manager.get_course_modules_list(_course_id)

            for i in range(1, min(len(course_modules),2)):
            
                if course_modules[i].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s1_users.txt') as f:
                        course_users_list = f.read().splitlines()
                    
                    for course_user in course_users_list:
                        if course_user == user.login:
                            return True

            return False

    def save_homework(self, _files_list, _id_room_chat, ):

        homework_service = HomeworkService()

        login_user = self.get_current_user().login

        homework_service.save_homework(_files_list, login_user, _id_room_chat)
    
    def get_user_list(self, _user_id):
        """
        Возвращает список пользователей

        Returns:
            List: список пользователей с типом User
        """

        user_manager = UserManager()
        users = user_manager.get_users(_user_id)

        return users
