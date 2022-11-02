from models.action_manager import ActionManager
from models.room_chat_manager import RoomChatManager
from models.user_manager import UserManager
from models.course_manager import EducationCourseManager
from models.education_stream_manager import EducationStreamManager
from models.homework_manager import HomeworkManager
from models.upload_manager import UploadManager
from models.users_file_manager import UsersFileManager

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

    def get_lesson(self, _user_id, _lesson_id, _id_course, _id_video, _type_lesson=None):
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

        if lesson is not None and _type_lesson is None:
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

        #education_streams = education_stream_manager.get_education_streams_list_by_login_user(user.login, user.role)

        #if _course_id is not None:
        #    for education_stream in education_streams:
        #        if education_stream.course == _course_id and education_stream.status == "идет":
        #            user.education_stream_list = education_stream

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

            # проверяем, есть ли пользователь в списках участников пятого потока
            for i in range(1, min(len(course_modules) + 1, 5)):
                if course_modules[i - 1].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s5_users.txt') as f:
                        course_users_list = f.read().splitlines()
                    
                    for course_user in course_users_list:
                        if course_user.split()[0].lower() == user.login:
                            return True

            # проверяем, есть ли пользователь в списках участников четвертого потока
            for i in range(1, min(len(course_modules) + 1, 9)):
                if course_modules[i - 1].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s4_users.txt') as f:
                        course_users_list = f.read().splitlines()
                    
                    for course_user in course_users_list:
                        if course_user.split()[0].lower() == user.login:
                            return True

            # проверяем, есть ли пользователь в списках участников третьего потока
            for i in range(1, min(len(course_modules) + 1, 9)):
                if course_modules[i - 1].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s3_users.txt') as f:
                        course_users_list = f.read().splitlines()
                    
                    for course_user in course_users_list:
                        if course_user.split()[0].lower() == user.login:
                            return True

            # проверяем, есть ли пользователь в списках участников второго потока
            for i in range(1, min(len(course_modules) + 1, 9)):
                if course_modules[i - 1].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s2_users.txt') as f:
                        course_users_list = f.read().splitlines()
                    
                    for course_user in course_users_list:
                        if course_user.split()[0] == user.login:
                            return True
            '''
            # проверяем, есть ли пользователь в спиках участкинов первого потока
            for i in range(1, min(len(course_modules) + 1, 9)):
                if course_modules[i - 1].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s1_users.txt') as f:
                        course_users_list = f.read().splitlines()
                    
                    for course_user in course_users_list:
                        if course_user.split()[0] == user.login:
                            return True
            '''

            return False

    def save_homework(self, _files_list, _id_room_chat, _current_user_id, _text, _id_lesson, _id_course):
        """
        Сохраняет домашнюю работу
        Args:
            _homework_files_list(Dict): данные сданной домашней работы
            _id_room_chat(Int): ID чата
            _text(String): ответ на задание
            _id_user(Int): ID пользователя
            _id_course(Int): ID курса
            _id_lesson(Int): ID урока

        Return:
            Homework: домашняя работа
        """

        homework_manager = HomeworkManager()
        user_manager = UserManager()
        upload_service = UploadManager()
        action_manager = ActionManager()
        course_manager = EducationCourseManager()

        login_user = user_manager.get_user_by_id(_current_user_id).login
        homework_files_list = upload_service.upload_files(_files_list, login_user)
        homework = homework_manager.create_homework(homework_files_list, _id_room_chat, _text, _current_user_id,
                                                    _id_course, _id_lesson)
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
        users_file_manager = UsersFileManager()
        room_chat_manager = RoomChatManager()
        user_manager = UserManager()

        homework_list = homework_manager.get_homeworks_list_by_id_room_chat(_id_room_chat)
        date = datetime.strptime("01/01/2000", "%d/%m/%Y")
        last_homework = None
        if homework_list != []:
            for homework in homework_list:
                if homework.id_user is None:
                    room_chat = room_chat_manager.get_room_chat(_id_room_chat)
                    name_room_chat = room_chat.name.split("_")
                    id_dict = {"course": int(name_room_chat[1]), "lesson": int(name_room_chat[2]),
                               "user": name_room_chat[3]}
                    if len(name_room_chat) > 4:
                        for i in range(0, len(name_room_chat) - 3):
                            if i + 4 < len(name_room_chat):
                                id_dict['user'] = "_".join([id_dict['user'], name_room_chat[i + 4]])
                            else:
                                break
                    homework.id_user = user_manager.get_user_by_login(id_dict['user']).user_id
                    homework.id_course = id_dict['course']
                    homework.id_lesson = id_dict['lesson']
                    homework_manager.update_homework(homework)

                if homework.date_delivery >= date:
                    date = homework.date_delivery
                    last_homework = homework

            files = users_file_manager.get_size_files(last_homework.users_files_list)
            last_homework.users_files_list = files

            return last_homework

    def get_last_homework(self, _id_course, _id_lesson, _id_user):

        user_manager = UserManager()
        room_chat_manager = RoomChatManager()

        user = user_manager.get_user_by_id(_id_user)
        id_room_chat = room_chat_manager.room_chat_entry(_id_course=_id_course, _id_lesson=_id_lesson,
                                                         _user=user, _id_room_chat=None, _id_module=None,
                                                         _id_education_stream=None).id

        return self.get_last_homework_by_id_room_chat(id_room_chat)

    def get_neighboring_lessons(self, _id_lesson, _id_course, _user_id):
        """
        Возвращает данные соседних уроков текущего урока

        Args:
            _user_id(Int): ID текущего пользователя
            _id_lesson(Int): ID текущего урока
            _id_course(Int): ID текущего курса

        Returns:
            Dict: данные соседних уроков текущего урока
        """

        course_manager = EducationCourseManager()

        neighboring_lessons = course_manager.get_neighboring_lessons(_id_lesson, _id_course)
        if neighboring_lessons['next_lesson'] is not None:
            available = self.is_course_module_avalable_for_user(_id_course, neighboring_lessons['next_lesson'].id, _user_id)
            if not available and neighboring_lessons['next_lesson'].id > 1:
                neighboring_lessons['next_lesson'] = None

        if neighboring_lessons['previous_lesson'] is not None:
            available = self.is_course_module_avalable_for_user(_id_course, neighboring_lessons['previous_lesson'].id, _user_id)
            if not available and neighboring_lessons['previous_lesson'].id > 1:
                neighboring_lessons['previous_lesson'] = None

        return neighboring_lessons