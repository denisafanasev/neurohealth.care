from flask import Markup

from services.homeworks_service import HomeworksService


class EducationHomeTasksPageController():
    """
    EducationHomeTasksPageController - класс контроллера представления списка домашних работ, реализующий логику взаимодействия приложения с пользователем.
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответствующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    # def get_homeworks_list(self, _id_current_user):
    #     """
    #     Возвращает список домашних работ пользователей
    #
    #     Returns:
    #         List: список домашних работ
    #     """
    #
    #     homework_service = HomeworksService()
    #
    #     homework_list = homework_service.get_homeworks_list()
    #     homework_list_view = []
    #     for homework in homework_list:
    #         lesson = homework_service.get_lesson(homework.id_lesson)
    #         course = homework_service.get_course(homework.id_lesson)
    #         # education_stream = homework_service.get_education_stream(room_chat.id_education_stream)
    #         user = homework_service.get_user_by_id(homework.id_user)
    #         room_chat = homework_service.get_room_chat(homework.id_lesson, homework.id_user, _id_current_user)
    #         if homework is not None:
    #             if homework.status is None:
    #                 homework.status = "Не проверено"
    #             elif homework.status:
    #                 homework.status = "Принято"
    #             else:
    #                 homework.status = "Не принято"
    #
    #         homework_view = {
    #             "id": homework.id,
    #             "user": {
    #                 "login": user.login,
    #                 "name": user.name
    #             },
    #             "course": {
    #                 "id": course.id,
    #                 "name": course.name
    #             },
    #             "lesson": {
    #                 "id": lesson.lessons.id,
    #                 "name": lesson.lessons.name,
    #                 "module_name": lesson.name
    #             },
    #             # "education_stream": {
    #             #     "id": education_stream.id,
    #             #     "name": education_stream.name
    #             # },
    #             "date_delivery": homework.date_delivery.strftime("%d/%m/%Y"),
    #             "users_files_list": homework.users_files_list,
    #             "status": homework.status,
    #             "text": Markup(homework.text)
    #         }
    #
    #         if room_chat is not None:
    #             homework_view['id_room_chat'] = room_chat.id
    #             homework_view['unread_message_amount'] = room_chat.unread_message_amount
    #
    #         homework_list_view.append(homework_view)
    #
    #     return homework_list_view

    def get_data(self, _id_current_user):
        """
        Возвращает данные курсов, домашних заданий и комнат чатов

        Args:
            _id_current_user(Integer): ID текущего пользователя

        Returns:
            List: данные
        """
        homeworks_service = HomeworksService()

        course_list = homeworks_service.get_courses_list()
        users_list = homeworks_service.get_users_list_in_education_streams()
        if course_list is not None:
            data_list = []
            for course in course_list:
                if course.type == "main":
                    if course.modules is not None:
                        for module in course.modules:
                            if module.lessons is not None:
                                for lesson in module.lessons:
                                    if lesson.task is not None:
                                        for user in users_list:
                                            homework_list = homeworks_service.get_homeworks_list_by_id_user(lesson.id,
                                                                                                            user.user_id)
                                            room_chat = homeworks_service.get_room_chat(lesson.id, user.user_id,
                                                                                        _id_current_user)
                                            data = {
                                                "user": {
                                                    "user_id": user.user_id,
                                                    "login": user.login,
                                                    "name": user.name
                                                },
                                                "course": {
                                                    "id": course.id,
                                                    "name": course.name
                                                },
                                                "module": {
                                                    "id": module.id,
                                                    "name": module.name
                                                },
                                                "lesson": {
                                                    "id": lesson.id,
                                                    "name": lesson.name,
                                                },
                                                "homework_list": None,
                                                "room_chat": None
                                            }
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
                                                        "users_files_list": homework.users_files_list,
                                                        "status": homework.status,
                                                        "text": Markup(homework.text)
                                                    }

                                                    data['homework_list'].append(homework)

                                            if room_chat is not None:
                                                data['room_chat'] = {
                                                    "id": room_chat.id,
                                                    "unread_message_amount": room_chat.unread_message_amount
                                                }

                                            if data['room_chat'] is not None:
                                                data_list.append(data)
                                            elif data['homework_list'] is not None:
                                                data_list.append(data)

            return data_list