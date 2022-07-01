from models.course_manager import CourseManager
from services.action_service import ActionService
from services.user_manager_service import UserManagerService
from models.user_manager import UserManager
from datetime import datetime
import config
class CourseService():
    """
    DownloadService - класс бизнес-логики сервиса управления настройками приложения
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def get_course_modules_list(self, _id):
        """
        Возвращает список модулей курса по id

        Args:
            _id(Int): индентификатор курса

        Returns:
            modules_list(List): списко модулей курса
        """

        course_manager = CourseManager()

        return course_manager.get_course_modules_list(_id)

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
        user_service = UserManagerService()

        login_user = user_service.get_current_user('').login
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

    # TODO: во все внутрении модули, id пользователя должен приезжать из app.py
    def get_current_user(self):
        """
        Возвращает объект User по id пользователя

        Args:
            _user_id   - Required  : id пользователя (Int)

        Returns:
            User: пользователь
        """

        user_service = UserManagerService()

        return user_service.get_current_user('')

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
        course_manager = CourseManager()
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
