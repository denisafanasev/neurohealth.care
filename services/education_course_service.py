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

        # если это обычный пользователь, посмотрим что за курс и модуль
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

            # проверяем, есть ли пользователь в списках участников второего потока
            for i in range(1, min(len(course_modules), 3)):
                if course_modules[i - 1].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s2_users.txt') as f:
                        course_users_list = f.read().splitlines()
                    
                    for course_user in course_users_list:
                        if course_user.split()[0] == user.login:
                            return True

            # проверяем, есть ли пользователь в спиках участкинов первого потока
            for i in range(1, min(len(course_modules), 7)):
                if course_modules[i - 1].id == _module_id:
                    with open(config.DATA_FOLDER + 'course_1/s1_users.txt') as f:
                        course_users_list = f.read().splitlines()
                    
                    for course_user in course_users_list:
                        if course_user.split()[0] == user.login:
                            return True

            return False

    # def get_last_homework_by_id_room_chat(self, _id_room_chat):
    #
    #     homework_manager = HomeworkManager()
    #     users_file_manager = UsersFileManager()
    #     room_chat_manager = RoomChatManager()
    #     user_manager = UserManager()
    #
    #     homework_list = homework_manager.get_homeworks_list_by_id_room_chat(_id_room_chat)
    #     date = datetime.strptime("01/01/2000", "%d/%m/%Y")
    #     last_homework = None
    #     if homework_list != []:
    #         for homework in homework_list:
    #             if homework.id_user is None:
    #                 room_chat = room_chat_manager.get_room_chat(_id_room_chat)
    #                 name_room_chat = room_chat.name.split("_")
    #                 id_dict = {"course": int(name_room_chat[1]), "lesson": int(name_room_chat[2]),
    #                            "user": name_room_chat[3]}
    #                 if len(name_room_chat) > 4:
    #                     for i in range(0, len(name_room_chat) - 3):
    #                         if i + 4 < len(name_room_chat):
    #                             id_dict['user'] = "_".join([id_dict['user'], name_room_chat[i + 4]])
    #                         else:
    #                             break
    #                 homework.id_user = user_manager.get_user_by_login(id_dict['user']).user_id
    #                 homework.id_course = id_dict['course']
    #                 homework.id_lesson = id_dict['lesson']
    #                 homework_manager.update_homework(homework)
    #
    #             if homework.date_delivery >= date:
    #                 date = homework.date_delivery
    #                 last_homework = homework
    #
    #         files = users_file_manager.get_size_files(last_homework.users_files_list)
    #         last_homework.users_files_list = files
    #
    #         return last_homework

    def get_last_homework(self, _id_course, _id_lesson, _id_user):
        """
        Возвращает последнее сданное домашнюю работу по уроку

        Args:
            _id_course(Int): ID курса
            _id_lesson(Int): ID урока
            _id_user(Int): ID пользователя

        Return:
            Homework: домашняя работа
        """

        user_manager = UserManager()
        room_chat_manager = RoomChatManager()

        user = user_manager.get_user_by_id(_id_user)
        # id_room_chat = room_chat_manager.room_chat_entry(_id_course=_id_course, _id_lesson=_id_lesson,
        #                                                  _user=user, _id_room_chat=None, _id_module=None,
        #                                                  _id_education_stream=None).id

        return
