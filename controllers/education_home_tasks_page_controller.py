import pandas as pd

from services.homeworks_service import HomeworksService


class EducationHomeTasksPageController():
    """
    EducationHomeTasksPageController - класс контроллера представления списка домашних работ, реализующий логику взаимодействия приложения с пользователем.
    Возвращает в слой отображения объекты в виде, пригодном для отображения в web странице и в соответствующем форматировании
    Взаимодейтвует с классами слоя сервисов, передавая им данные и получая данные в объектах доменной модели
    """

    def get_homework_no_verified(self, _id_current_user, _id_education_stream, _id_user):
        """
        Возвращает данные курсов и домашних заданий

        Args:
            _id_current_user(Integer): ID текущего пользователя
            _id_education_stream(Integer): ID образовательного потока
            _id_user(Integer): ID пользователя, чьи ответы на домашние работы запросили

        Returns:
            List: данные
        """
        homeworks_service = HomeworksService()

        if _id_user is None:
            return None

        user = homeworks_service.get_user_by_id(_id_user)
        education_stream = homeworks_service.get_education_stream(_id_education_stream)
        data_list = []
        if homeworks_service.is_there_homework_in_sql():
            homework_list = homeworks_service.get_homeworks_list_by_id_user_no_verified(education_stream.course.id,
                                                                                        user.user_id)
            for homework in homework_list:
                homework_chat = homeworks_service.get_homework_chat(homework['doc_id_lesson'], user.user_id,
                                                                    _id_current_user)
                data = self.get_view_data_from_sql(homework, homework_chat)
                data_list.append(data)

        else:
            lessons_list = homeworks_service.get_lessons_by_id_course(education_stream.course.id)
            for lesson in lessons_list:
                module = homeworks_service.get_module_by_id(lesson.id_module)
                homework_list = homeworks_service.get_homeworks_list_by_id_user_no_verified(lesson.id, user.user_id)
                if homework_list is None:
                    continue

                homework_chat = homeworks_service.get_homework_chat(lesson.id, user.user_id, _id_current_user)
                data = self.get_view_data_from_nosql(homework_list, homework_chat, module, lesson)

                data_list.append(data)

        return data_list

    def get_chat_without_homework(self, _id_current_user, _id_education_stream, _id_user):
        """
        Возвращает чаты, по урокам которых не были сданы домашние работы

        Args:
            _id_current_user(Integer): ID текущего пользователя
            _id_education_stream(Integer): ID образовательного потока
            _id_user(Integer): ID пользователя, чьи ответы на домашние работы запросили

        Returns:
            List: данные
        """
        homeworks_service = HomeworksService()

        user = homeworks_service.get_user_by_id(_id_user)
        education_stream = homeworks_service.get_education_stream(_id_education_stream)
        data_list = []
        if homeworks_service.is_there_homework_in_sql():
            homeworks_chat_list = homeworks_service.get_homeworks_chats_list_by_id_user(_id_user=user.user_id,
                                                                                        _id_course=education_stream.course.id)
            for homework_chat in homeworks_chat_list:
                data = self.get_view_data_from_sql(_homework_chat=homework_chat)
                data_list.append(data)


        else:
            lessons_list = homeworks_service.get_lessons_by_id_course(education_stream.course.id)

            for lesson in lessons_list:
                module = homeworks_service.get_module_by_id(lesson.id_module)
                homeworks_chat_list = homeworks_service.get_homeworks_list_by_id_user_verified(_id_lesson=lesson.id,
                                                                                               _id_user=user.user_id)
                if homeworks_chat_list is not None:
                    continue

                homework_chat = homeworks_service.get_homework_chat(lesson.id, user.user_id, _id_current_user)
                if homework_chat is None:
                    continue

                data = self.get_view_data_from_nosql(homeworks_chat_list, homework_chat, module, lesson)

                data_list.append(data)

        return data_list

    def get_homework_verified(self, _id_current_user, _id_education_stream, _id_user):
        """
        Возвращает данные проверенных домашних работ пользователя

        Args:
            _id_current_user(Integer): ID текущего пользователя
            _id_education_stream(Integer): ID образовательного потока
            _id_user(Integer): ID пользователя, чьи ответы на домашние работы запросили

        Returns:
            List: данные
        """
        homeworks_service = HomeworksService()

        user = homeworks_service.get_user_by_id(_id_user)
        education_stream = homeworks_service.get_education_stream(_id_education_stream)
        data_list = []
        if homeworks_service.is_there_homework_in_sql():
            # если для хранения домашних работ используется postgresql, то мы проходимся по домашним работам
            homework_list = homeworks_service.get_homeworks_list_by_id_user_verified(user.user_id,
                                                                                     _id_course=education_stream.course.id)
            homework_chats_df = homeworks_service.get_homework_chat_by_course(education_stream.course.id, _id_user,
                                                                              _id_current_user)

            data_list = self.get_view_data_from_sql_test(homework_list, homework_chats_df)
            # data_list = homework_list.applymap(lambda x: self.get_view_data_from_sql(x, homework_chats_df))
            # for homework in homework_list:
                # homework_chat = homeworks_service.get_homework_chat(homework['doc_id_lesson'], user.user_id,
                #                                                     _id_current_user)
                # data = self.get_view_data_from_sql(homework, homework_chat)
                # data_list.append(data)

        else:
            # если нет, то проходимся по каждому уроку и проверяем домашние работы
            lessons_list = homeworks_service.get_lessons_by_id_course(education_stream.course.id)
            for lesson in lessons_list:
                module = homeworks_service.get_module_by_id(lesson.id_module)
                homework_list = homeworks_service.get_homeworks_list_by_id_user_verified(lesson.id, user.user_id)
                if homework_list is None:
                    continue

                homework_chat = homeworks_service.get_homework_chat(lesson.id, user.user_id, _id_current_user)
                data = self.get_view_data_from_nosql(homework_list, homework_chat, module, lesson)

                data_list.append(data)

        return data_list

    def get_view_data_from_sql_test(self, _homework: pd.DataFrame, _homework_chat):
        """
        Возвращает представление домашних работ, чатов, модулей и уроков пользователя (данный из postgresql)

        Args:
            _homework(List): список домашних работ по уроку
            _homework_chat(HomeworkChat): чат

        Returns:
            data_view: представление данных
        """

        data_view = {'homework_list': []}
        if _homework is not None:
            _homework['status'] = _homework['status'].apply(lambda x: "Не проверено" if x is None else x)
            _homework['status'] = _homework['status'].apply(lambda x: "Принято" if x is True else x)
            _homework['status'] = _homework['status'].apply(lambda x: "Не принято" if x is False else x)
            pd.to_datetime(_homework['date_delivery'], format='%d/%m/%Y', dayfirst=True)

        else:
            data_view['homework_list'] = None

        if _homework_chat is not None:
            _homework_chat = _homework_chat.rename(columns={'doc_id': 'id'})
            _homework_chat['unread_message_amount'] = _homework_chat['unread_message_amount'].apply(lambda x: 0 if x is None else x)

        if _homework is not None and _homework_chat is not None:
            data = pd.merge(_homework, _homework_chat, how='outer', on=['doc_id_lesson', 'id_user'])

            data_df = pd.DataFrame()
            data_df_homeworks = data[['status', 'date_delivery', 'doc_id']]
            data_df_homeworks = data_df_homeworks.rename(columns={'doc_id': 'id'})
            data_df['homework_list'] = data_df_homeworks.to_dict('records')

            data_df['homework_chat'] = data[['unread_message_amount', 'id']].to_dict('records')

            data_df_module = data[['doc_id_module_x', 'name_module_x']]
            data_df_module = data_df_module.rename(columns={'name_module_x': 'name', 'doc_id_module_x': 'id'})
            data_df['module'] = data_df_module.to_dict('records')

            data_df_lesson = data[['doc_id_lesson', 'name_lesson_x']]
            data_df_lesson = data_df_lesson.rename(columns={'name_lesson_x': 'name', 'doc_id_lesson': 'id'})
            data_df['lesson'] = data_df_lesson.to_dict('records')

            data_view = data_df.to_dict('records')

        else:
            data_view['homework_chat'] = None

        return data_view

    def get_view_data_from_sql(self, _homework=None, _homework_chat=None):
        """
        Возвращает представление домашних работ, чатов, модулей и уроков пользователя (данный из postgresql)

        Args:
            _homework(List): список домашних работ по уроку
            _homework_chat(HomeworkChat): чат

        Returns:
            data_view: представление данных
        """

        data_view = {'homework_list': []}
        # if _homework_list is None:
        #     data_view['homework_list'] = None
        # else:
        if _homework is not None:
            if _homework['status'] is None:
                _homework['status'] = "Не проверено"
            elif _homework['status']:
                _homework['status'] = "Принято"
            else:
                _homework['status'] = "Не принято"

            homework = {
                "id": _homework['doc_id'],
                "date_delivery": _homework['date_delivery'].strftime("%d/%m/%Y"),
                "status": _homework['status'],
            }

            data_view['homework_list'].append(homework)

        else:
            data_view['homework_list'] = None

        if _homework_chat is not None:
            data_view['homework_chat'] = {"id": _homework_chat['doc_id']}
            if _homework_chat['unread_message_amount'] is None:
                data_view['homework_chat']['unread_message_amount'] = 0
            else:
                data_view['homework_chat']['unread_message_amount'] = _homework_chat['unread_message_amount']
        else:
            data_view['homework_chat'] = None

        if data_view.get('homework_list') is not None or data_view.get('homework_chat') is not None:
            data_view['module'] = {
                "id": _homework['doc_id_module'],
                "name": _homework['name_module']
            }
            data_view['lesson'] = {
                "id": _homework['doc_id_lesson'],
                "name": _homework['name_lesson'],
            }

        return data_view

    def get_view_data_from_nosql(self, _homework_list, _homework_chat, _module, _lesson):
        """
        Возвращает представление домашних работ, чатов, модулей и уроков пользователя (данные из tinydb)

        Args:
            _homework_list(List): список домашних работ по уроку
            _homework_chat(HomeworkChat): чат
            _module(Module): модуль
            _lesson(Lesson): урок, по которому сдали домашние работы пользователь

        Returns:
            data_view: представление данных
        """

        data_view = {'homework_list': []}
        if _homework_list is None:
            data_view['homework_list'] = None
        else:
            for homework in _homework_list:
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

                data_view['homework_list'].append(homework)

        if _homework_chat is not None:
            data_view['homework_chat'] = {
                "id": _homework_chat.id,
                "unread_message_amount": _homework_chat.unread_message_amount
            }
        else:
            data_view['homework_chat'] = None

        if data_view['homework_list'] is not None or data_view['homework_chat'] is not None:
            data_view['module'] = {
                "id": _module.id,
                "name": _module.name
            }
            data_view['lesson'] = {
                "id": _lesson.id,
                "name": _lesson.name,
            }

        return data_view

    def get_education_streams_list(self):
        """
        Возвращает список данных всех обучающих потоков

        Returns:
            List(): список образовательных потоков
        """
        homeworks_service = HomeworksService()

        education_streams_list = homeworks_service.get_educations_stream()
        education_streams_list_view = []
        for education_stream in education_streams_list:
            education_stream_view = {
                "id": education_stream.id,
                'name': education_stream.name,
            }

            education_streams_list_view.append(education_stream_view)

        return education_streams_list_view

    def get_current_education_stream(self, _id_education_stream, _current_user_id):
        """
        Возвращает данные текущего потока потока

        Args:
            _id_education_stream(Int): ID образовательного потока
            _current_user_id

        Returns:
            List: список пользователей
        """

        homeworks_service = HomeworksService()

        education_stream = homeworks_service.get_education_stream(_id_education_stream)
        education_stream_view = {
            'id': education_stream.id,
            'name': education_stream.name,
            'students_list': [],
            'course_name': education_stream.course.name
        }
        lessons_list = homeworks_service.get_lessons_by_id_course(education_stream.course.id)
        id_lessons_list = set(lesson.id for lesson in lessons_list)
        for user_data in education_stream.students_list:
            user_view = {
                "user_id": user_data.user_id,
                'name': user_data.name
            }
            # проверяем есть ли непрочитанные сообщения у текущего пользователя и
            # сколько принято/не принято домашних работ у пользователей потока
            user_view['is_unread_message'] = homeworks_service.is_unread_messages(id_lessons_list, user_data.user_id,
                                                                                  education_stream.course.id)

            user_view['amount_accepted_homeworks'], user_view['amount_no_accepted_homeworks'] = \
                homeworks_service.get_amount_accepted_homework(user_data.user_id, id_lessons_list,
                                                               education_stream.course.id)
            education_stream_view['students_list'].append(user_view)

        return education_stream_view

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
            'user_id': user.user_id,
            'name': user.name
        }

        return user_view
