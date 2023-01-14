from flask import Markup

from services.homeworks_service import HomeworksService


class EducationHomeTasksPageController():
    """
    EducationHomeTasksPageController - класс контроллера представления списка домашних работ, реализующий логику взаимодействия приложения с пользователем.
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответствующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    def get_data(self, _id_current_user, _id_education_stream, _id_user):
        """
        Возвращает данные курсов и домашних заданий

        Args:
            _id_current_user(Integer): ID текущего пользователя
            _id_education_stream(Integer): ID образовательного потока

        Returns:
            List: данные
        """
        homeworks_service = HomeworksService()
        if _id_user is None:
            return None
        user = homeworks_service.get_user_by_id(_id_user)
        lessons_list = homeworks_service.get_lessons()
        data_list = []
        for lesson in lessons_list:
            module = homeworks_service.get_module_by_id(lesson.id_module)
            course = homeworks_service.get_course_by_id(module.id_course)
            homework_list = homeworks_service.get_homeworks_list_by_id_user_no_verified(lesson.id, user.user_id)
            if homework_list is None:
                continue

            homework_chat = homeworks_service.get_homework_chat(lesson.id, user.user_id, _id_current_user)
            data = {}
            if homework_list is not None:
                data['homework_list'] = []
                for homework in homework_list:
                    if homework is not None:
                        if homework.status is None:
                            homework.status = "Не проверено"
                        elif homework.status:
                            homework.status = "Принято"
                        else:
                            homework.status = "Не принято"
                    homework = {
                        "id": homework.id,
                        "date_delivery": homework.date_delivery.strftime("%d/%m/%Y"),
                        "status": homework.status,
                    }

                    data['homework_list'].append(homework)

            else:
                continue

            if homework_chat is not None:
                data['homework_chat'] = {
                    "id": homework_chat.id,
                    "unread_message_amount": homework_chat.unread_message_amount
                }
            else:
                data['homework_chat'] = None

            if data['homework_list'] is not None or data['homework_chat'] is not None:
                data['module'] = {
                    "id": module.id,
                    "name": module.name
                }
                data['lesson'] = {
                    "id": lesson.id,
                    "name": lesson.name,
                }

                data_list.append(data)

        course_name = course.name

        return data_list, course_name

    def get_chat_without_homework(self, _id_current_user, _id_education_stream, _id_user):
        """
        Возвращает данные курсов, домашних заданий и чатов

        Args:
            _id_current_user(Integer): ID текущего пользователя
            _id_education_stream(Integer): ID образовательного потока

        Returns:
            List: данные
        """
        homeworks_service = HomeworksService()
        user = homeworks_service.get_user_by_id(_id_user)
        lessons_list = homeworks_service.get_lessons()
        data_list = []
        for lesson in lessons_list:
            module = homeworks_service.get_module_by_id(lesson.id_module)
            course = homeworks_service.get_course_by_id(module.id_course)
            homework_list = homeworks_service.get_homeworks_list_by_id_user_verified(lesson.id, user.user_id)
            if homework_list is not None:
                continue

            homework_chat = homeworks_service.get_homework_chat(lesson.id, user.user_id, _id_current_user)
            if homework_chat is None:
                continue

            data = {}
            data['homework_list'] = None
            data['homework_chat'] = {
                "id": homework_chat.id,
                "unread_message_amount": homework_chat.unread_message_amount
            }
            data['module'] = {
                "id": module.id,
                "name": module.name
            }
            data['lesson'] = {
                "id": lesson.id,
                "name": lesson.name,
            }

            data_list.append(data)

        course_name = course.name

        return data_list, course_name

    def get_homework_verified(self, _id_current_user, _id_education_stream, _id_user):
        """
        Возвращает данные курсов, домашних заданий и чатов

        Args:
            _id_current_user(Integer): ID текущего пользователя
            _id_education_stream(Integer): ID образовательного потока

        Returns:
            List: данные
        """
        homeworks_service = HomeworksService()
        user = homeworks_service.get_user_by_id(_id_user)
        lessons_list = homeworks_service.get_lessons()
        data_list = []
        for lesson in lessons_list:
            module = homeworks_service.get_module_by_id(lesson.id_module)
            course = homeworks_service.get_course_by_id(module.id_course)
            homework_list = homeworks_service.get_homeworks_list_by_id_user_verified(lesson.id, user.user_id)
            if homework_list is None:
                continue

            homework_chat = homeworks_service.get_homework_chat(lesson.id, user.user_id, _id_current_user)
            data = {}
            if homework_list is not None:
                data['homework_list'] = []
                for homework in homework_list:
                    if homework is not None:
                        if homework.status:
                            homework.status = "Принято"
                        else:
                            homework.status = "Не принято"

                    homework = {
                        "id": homework.id,
                        "date_delivery": homework.date_delivery.strftime("%d/%m/%Y"),
                        "status": homework.status,
                    }

                    data['homework_list'].append(homework)

            else:
                continue

            if homework_chat is not None:
                data['homework_chat'] = {
                    "id": homework_chat.id,
                    "unread_message_amount": homework_chat.unread_message_amount
                }
            else:
                data['homework_chat'] = None

            if data['homework_list'] is not None or data['homework_chat'] is not None:
                data['course'] = {
                    "id": course.id,
                    "name": course.name
                }
                data['module'] = {
                    "id": module.id,
                    "name": module.name
                }
                data['lesson'] = {
                    "id": lesson.id,
                    "name": lesson.name,
                }

                data_list.append(data)

        course_name = course.name

        return data_list, course_name

    def get_education_streams_list(self):
        """
        Возвращает список данных всех обучающих потоков

        Returns:
            List(): список образовательных потоков
        """
        homeworks_service = HomeworksService()

        education_streams_list = homeworks_service.get_educations_stream()
        education_streams_list_view =[]
        for education_stream in education_streams_list:
            education_stream_view = {
                "id": education_stream.id,
                'name': education_stream.name,
            }

            education_streams_list_view.append(education_stream_view)

        return education_streams_list_view

    def get_users_list_by_id_education_stream(self, _id_education_stream, _current_user_id):
        """
        Возвращает список пользователей данного потока

        Args:
            _id_education_stream(Int): ID образовательного потока
            _current_user_id

        Returns:
            List: список пользователей
        """

        homework_service = HomeworksService()

        users_list = homework_service.get_users_list_in_education_streams_file(_id_education_stream)
        lessons_list = homework_service.get_lessons()
        users_list_view = []
        for user_data in users_list:
            user_view = {
                "id": user_data.user_id,
                'name': user_data.name
            }
            for lesson in lessons_list:
                user_view['is_unread_message'] = homework_service.is_unread_messages(lesson.id, user_data.user_id, _current_user_id)
                if user_view['is_unread_message']:
                    break

            users_list_view.append(user_view)

        return users_list_view

    def get_user(self, _user_id):
        """
        Возвращает данные пользователя, чьи домашние задания запросили

        Args:
            _user_id(Int): ID

        Returns:
            Dict: данные пользователя
        """

        homeworks_service = HomeworksService()

        user = homeworks_service.get_user_by_id(_user_id)
        user_view = {
            'id': user.user_id,
            'name': user.name
        }

        return user_view