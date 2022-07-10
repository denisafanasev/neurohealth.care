#TODO: передалать на использование менеджера и не сервиса
from models.action_manager import ActionManager
from models.room_chat_manager import RoomChatManager
from models.user_manager import UserManager
from models.course_manager import EducationCourseManager
from models.education_stream_manager import EducationStreamManager
from models.homework_manager import HomeworkManager
from models.upload_manager import UploadManager

from datetime import datetime
import config


class EducationCourseService():
    """
    EducationCourseService - класс бизнес-логики сервиса управления настройками приложения
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

        course_manager = EducationCourseManager()

        modules_list = course_manager.get_course_modules_list(_id)

        return modules_list

    def get_lesson(self, _user_id, _lesson_id, _id_course, _id_video):
        """
        Возвращает данные урока

        Args:
            _lesson_id(Int): индентификатор урока
            _id_course(Int): индентификатор курса
            _id_video(Int): индентификатор видео
            _user_id(Int): индетификатор текущего пользователя в системе

        Return:
            Lesson: класс Lesson, обернутый в класс Module
        """

        course_manager = EducationCourseManager()
        user_manager = UserManager()
        action_manager = ActionManager()

        login_user = user_manager.get_user_by_id(_user_id).login
        lesson = course_manager.get_lesson(_lesson_id, _id_course, _id_video)

        action_manager.add_notifications(lesson, "посмотрел", '', "course_manager", login_user)

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

            for i in range(1, min(len(course_modules), 4)):
                if course_modules[i - 1].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s1_users.txt') as f:
                        course_users_list = f.read().splitlines()
                    
                    for course_user in course_users_list:
                        if course_user.split()[0] == user.login:
                            return True

            return False

    def save_homework(self, _files_list, _id_room_chat, _current_user_id, _text, _id_lesson, _id_course):
        """
        Сохраняет домашнюю работу

        Args:
            _files_list(List): список файлов, отправленных пользователем
            _current_user_id(Int): ID текущего пользователя
            _id_room_chat(Int): ID комнаты чата
        """

        homework_manager = HomeworkManager()
        user_manager = UserManager()
        upload_service = UploadManager()
        action_manager = ActionManager()
        course_manager = EducationCourseManager()

        login_user = user_manager.get_user_by_id(_current_user_id).login
        homework_files_list = upload_service.upload_files(_files_list, login_user)
        homework = homework_manager.create_homework(homework_files_list, _id_room_chat, _text)
        lesson = course_manager.get_lesson(_id_lesson, _id_course)

        homework_manager.create_homework_answer(homework.id)
        action_manager.add_notifications("", "сдал", lesson.lessons.name, "homework_manager", login_user)

    def get_user_list(self, _user_id):
        """
        Возвращает список пользователей

        Args:
            _user_id(Int): ID пользователя

        Returns:
            List: список пользователей с типом User
        """

        user_manager = UserManager()
        users = user_manager.get_users(_user_id)

        return users

    def room_chat_entry(self, _id_lesson, _id_course, _id_user, _id_room_chat, _id_education_stream, _id_module):
        """
        Подключает пользователя к чату

        Args:
            _id_lesson(Int): индентификатор урока
            _id_user(User): ID пользователя
            _id_course(Int): индентификатор курса
            _id_room_chat(Int): индентификатор чата

        Returns:
            RoomChat: чат
        """

        room_chat_manager = RoomChatManager()
        user_manager = UserManager()

        user = user_manager.get_user_by_id(_id_user)

        return room_chat_manager.room_chat_entry(_id_lesson, user, _id_course, _id_room_chat, _id_education_stream,
                                                 _id_module)

    def add_message(self, _message, _room_chat_id, _user_id):
        """
        Сохраняет сообщение

        Args:
            _message(Dict): данные сообщения
            _room_chat_id(Int): индентификатор чата
        """

        room_chat_manager = RoomChatManager()
        user_manager_service = UserManager()

        _message["name_sender"] = user_manager_service.get_user_by_id(_user_id).login

        return room_chat_manager.add_message(_message, _room_chat_id)

    def get_last_homework_by_id_room_chat(self, _id_room_chat):

        homework_manager = HomeworkManager()

        homework_list = homework_manager.get_homeworks_list_by_id_room_chat(_id_room_chat)
        date = datetime.strptime("01/01/2000", "%d/%m/%Y")
        last_homework = None
        if homework_list != []:
            for homework in homework_list:
                if homework.date_delivery >= date:
                    date = homework.date_delivery
                    last_homework = homework

            return last_homework

    def get_last_homework(self, _id_course, _id_lesson, _id_user):

        user_manager = UserManager()
        room_chat_manager = RoomChatManager()

        user = user_manager.get_user_by_id(_id_user)
        id_room_chat = room_chat_manager.room_chat_entry(_id_course=_id_course, _id_lesson=_id_lesson,
                                                         _user=user, _id_room_chat=None, _id_module=None,
                                                         _id_education_stream=None).id

        return self.get_last_homework_by_id_room_chat(id_room_chat)
