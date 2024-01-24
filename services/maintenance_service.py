import os
from distutils.command.config import config

import pandas as pd
from sqlalchemy import text, create_engine

from models.action_manager import ActionManager
from models.homework_chat_manager import HomeworkChatManager
from models.message_manager import MessageManager
from models.course_manager import EducationCourseManager
from models.homework_manager import HomeworkManager
from models.module_manager import EducationModuleManager
from models.lesson_manager import EducationLessonManager
from models.user_manager import UserManager
from data_adapters.data_store import DataStore

import config


class MaintenanceService():
    """
    Service for maintenance page
    """

    def init(self):
        """
        Constructor
        """
        pass

    # def get_upload_users_from_json_to_sql_page_data(self, _current_user_id):
    #     """
    #     Get data for page view
    #
    #     Args:
    #         _current_user_id (Int): id of current user looged into the system
    #     """
    #     _data = []
    #
    #     data_store_tinydb = DataStore('users')
    #     users_number = data_store_tinydb.get_rows_count()
    #
    #     data_store_postgresql = DataStore("users", force_adapter="PostgreSQLDataAdapter")
    #     current_data_adapter = data_store_postgresql.current_data_adapter
    #     if current_data_adapter == 'PostgreSQLDataAdapter':
    #         db_users_number = data_store_postgresql.get_rows_count()
    #         is_there_table = 'Created'
    #     else:
    #         db_users_number = None
    #         is_there_table = 'No created'
    #
    #     _data = {}
    #     _data["data_folder"] = config.DATA_FOLDER
    #     _data["users_number"] = users_number
    #     _data["PostgreSQLDataAdapter_connection_string"] = config.PostgreSQLDataAdapter_connection_string()
    #     _data["current_data_adapter"] = current_data_adapter
    #     _data["db_users_number"] = db_users_number
    #     _data["is_there_table"] = is_there_table
    #
    #     return _data

    def add_row_to_sql(self, _data_store, _id, _data_row):

        if _data_store.get_row_by_id(_id) is None:

            # _data_store.update_row_by_id(_data_row, _id)
            # if data non existed, make insert of a new row
            _data_store.insert_row(_data_row)

    # def is_superuser(self, func):
    #     def wrapper(*args):
    #         user_manager = UserManager()
    #         if user_manager.get_user_role(args[0]) == 'superuser':
    #             func()
    #         else:
    #             raise UserManagerException('У вас нет доступа')
    #
    #     return wrapper


    def upload_users_from_json_to_sql(self, _current_user_id):
        """
        Uploads users from json file to sql
        @params:
        """

        # get all users in the system
        user_manager = UserManager()
        data_store_tiny_db = DataStore('users')
        if user_manager.get_user_role(_current_user_id) == 'superuser':
            users = data_store_tiny_db.get_rows()
        else:
            users = []

        # create data store with SQL data adapter
        data_store = DataStore("users", force_adapter="PostgreSQLDataAdapter")
        for user_data in users:
            user = user_manager.user_row_to_user(user_data)
            if user.token == '':
                user.token = user_manager.create_token(user.email)
            # convert User object to Dict
            user_raw = {"doc_id": user.user_id, "active": user.active, "password": user_data['password'],
                        "created_date": user.created_date,
                        "education_module_expiration_date": user.education_module_expiration_date, "email": user.email,
                        "email_confirmed": user.email_confirmed, "login": user.login, "name": user.name,
                        "probationers_number": user.probationers_number, "role": user.role, "token": user.token}

            self.add_row_to_sql(data_store, user.user_id, user_raw)

            # if data_store.get_row_by_id(user.user_id):
            #
            #     # if user existed in the table, make change
            #     data_store.update_row_by_id(user_raw, user.user_id)
            #
            # else:
            #
            #     # if user non existed, make insert of a new row
            #     data_store.insert_row(user_raw)

    def get_upload_actions_from_json_to_sql_page_data(self, _current_user_id) -> dict:
        """
        Get data for page view

        Args:
            _current_user_id (Int): id of current user looged into the system
        """
        actions_number = 0
        # create list file names in DATA_FOLDER
        file_list = os.listdir(os.path.join(config.DATA_FOLDER))
        for name_file in file_list:
            # choose files with user actions data
            if 'action.json.' in name_file:
                name_file_list = name_file.split('.')
                action_name_fixed_file = f'action.save.{name_file_list[-1]}.json'
                if action_name_fixed_file in file_list:
                    continue
                action_name_file = self.fixed_action_file(name_file).replace('.json', '')

            elif 'action.json' == name_file:
                action_name_file = 'action'

            elif 'action.save' in name_file:
                action_name_file = name_file.replace('.json', '')

            else:
                continue
            # sum number of data from files
            data_store_tinydb = DataStore(action_name_file)
            actions_number += data_store_tinydb.get_rows_count()

        # get number of data from PostgreSQL and check if the table has been created
        data_store_postgresql = DataStore("action", force_adapter="PostgreSQLDataAdapter")
        current_data_adapter = data_store_postgresql.current_data_adapter
        if current_data_adapter == 'PostgreSQLDataAdapter':
            db_actions_number = data_store_postgresql.get_rows_count()
            is_there_table = 'Created'
        else:
            db_actions_number = None
            is_there_table = 'No created'

        _data = {}
        _data["data_folder"] = config.DATA_FOLDER
        _data["actions_number"] = actions_number
        _data["PostgreSQLDataAdapter_connection_string"] = config.PostgreSQLDataAdapter_connection_string()
        _data['current_data_adapter'] = data_store_postgresql.current_data_adapter
        _data["db_actions_number"] = db_actions_number
        _data['is_there_table'] = is_there_table

        return _data

    def upload_actions_from_json_to_sql(self) -> None:
        """
        Uploads actions  from json file to sql
        """

        action_manager = ActionManager()
        # create list of name file in directory
        file_list = os.listdir(os.path.join(config.DATA_FOLDER))
        # create data store with SQL data adapter
        data_store = DataStore('users', force_adapter='PostgreSQLDataAdapter')
        # create database connection
        con = create_engine("postgresql:" + config.PostgreSQLDataAdapter_connection_string())
        # create a list of file names with user actions data
        actions_files_list = sorted([file for file in file_list if 'action.save' in file or 'action.json' == file])
        # create DataFrame with users data(login and user_id)
        users_list = data_store.get_rows()
        users_df = pd.DataFrame(users_list)
        users_df = users_df[['login', 'doc_id']]
        action_data_store = DataStore('action', force_adapter='PostgreSQLDataAdapter')

        for action_file in actions_files_list:
            actions_list = action_data_store.get_rows()
            actions_df = None
            if actions_list:
                actions_df = pd.DataFrame(actions_list)
                actions_df.drop(columns=['doc_id'], inplace=True)
                actions_df['created_date'] = pd.to_datetime(actions_df['created_date']).dt.strftime(
                    '%d-%m-%Y %H:%M:%S')

        for action_file in actions_files_list:
            # retrieve data from the file
            actions_json_df = self.get_json_data_in_dataframe(action_file)
            # merge DataFrame with user actions data and users data
            actions_old_df = pd.merge(actions_json_df, users_df, how='left', on=['login'])
            # print(f'action_json_df {action_file}: {len(actions_json_df)}')

            # remove unnecessary columns
            actions_old_df.rename(columns={'doc_id': 'user_id'}, inplace=True)
            actions_with_none = actions_old_df['user_id'].isnull()
            # If, when merging tables for actions, the user who performed them is not found,
            # we go through each of them separately
            if True in actions_with_none.values:
                actions_with_none = actions_with_none[actions_with_none == True]
                delete_index_list = []
                for index in actions_with_none.keys():
                    user = data_store.get_rows(
                        {'where': f"login = '{actions_old_df['login'][index].replace(' ', '')}'"})
                    if user:
                        # If the user is found, we record the user
                        actions_old_df['user_id'][index] = user[0]['doc_id']
                    else:
                        # Otherwise, write the index of the action to the list and then delete the action
                        delete_index_list.append(index)

                actions_old_df = actions_old_df.drop(delete_index_list)
                # print(f'Незаписанные: {delete_index_list}')

            actions_old_df = actions_old_df.drop(['login', 'id'], axis=1)
            # if actions_df is not None:
            #     actions_old_df = pd.concat([actions_df, actions_old_df], join='outer')
            if actions_df is not None:
                actions_old_df['created_date'] = pd.to_datetime(actions_old_df['created_date']).dt.strftime(
                    '%d-%m-%Y %H:%M:%S')
                actions_old_df = pd.merge(actions_df, actions_old_df, how='outer', indicator=True, on='created_date')
                actions_old_df.drop(actions_old_df[actions_old_df['_merge'] != 'right_only'].index, inplace=True)
                actions_old_df.drop(columns=['_merge', 'user_id_x', 'action_x', 'comment_action_x'], axis=1,
                                    inplace=True)
                actions_old_df.rename(
                    columns={'user_id_y': 'user_id', 'action_y': 'action', 'comment_action_y': 'comment_action'},
                    inplace=True)

                # actions_old_df.index += len(actions_df)
            # print(f'actions_old_df {action_file}: {len(actions_old_df)}')
            # print(f'разница: {len(actions_json_df) - len(actions_old_df)}\n')

            actions_old_df.index += 1
            # import user actions data into PostgreSQL
            actions_old_df.to_sql('action', con, if_exists='append', index_label='doc_id')

    def create_table_in_sql(self, _table_name: str) -> None:
        """
        Создает таблицу в PostgreSQL

        Args:
            _table_name(Str): имя таблицы

        Returns:
            None
        """
        # Подключаемся к БД
        data_store = DataStore(None, force_adapter="PostgreSQLDataAdapter")
        # Читаем файл, в котором есть sql скрипты для создания таблиц
        with open('database/neurohealth.sql', 'r') as sql_file:
            sql_text = sql_file.read()

        sql_scripts_list = sql_text.split('\n\n')
        # Ищем нужный и после создаем таблицу
        for sql_script in sql_scripts_list:
            if _table_name in sql_script:
                data_store.data_store.data_store.execute(text(sql_script))
                break

    def fixed_action_file(self, _name_file: str) -> str:
        """
        Исправляет поврежденный файл json, в котором хранятся действия пользователя и возвращает новое имя этого файла

        Args:
            _name_file(str): имя файла, который нужно исправить

        Returns:
            action_name_file(Str): новое имя
        """
        with open(config.DATA_FOLDER + _name_file, 'r', encoding='utf8') as action_file:
            actions = action_file.read()
            if '\x00' in actions:
                actions = actions.replace('\x00', '')

            while actions[-1] != '}':
                actions = actions[:-1]

            if not actions.endswith('}}}'):
                count = actions[-3:].count('}')
                actions += '}' * (3 - count)

        name_file_list = _name_file.split('.')
        action_name_file = f'action.save.{name_file_list[-1]}.json'
        # os.rename(os.path.join(config.DATA_FOLDER, _name_file), action_name_file)
        with open(config.DATA_FOLDER + action_name_file, 'w', encoding='utf8') as action_file:
            action_file.write(actions)

        return action_name_file

    def upload_courses_list_from_json_to_sql(self) -> None:
        """
        Uploads courses list from json file to sql
        @params:
        """

        # get all courses in the system
        course_manager = EducationCourseManager()
        data_store_tiny_db = DataStore('courses_list')

        courses_list_data = data_store_tiny_db.get_rows()
        # create data store with SQL data adapter
        data_store = DataStore("courses_list", force_adapter="PostgreSQLDataAdapter")
        for course_data in courses_list_data:
            # convert Course object to Dict
            course = course_manager.course_row_to_course(course_data)
            course_raw = {
                'doc_id': course.id,
                'name': course.name,
                'description': course.description,
                'type': course.type,
                'image': course.image
            }

            self.add_row_to_sql(data_store, course.id, course_raw)

    def upload_modules_list_from_json_to_sql(self) -> None:
        """
        Uploads courses list from json file to sql
        @params:
        """

        # get all courses in the system
        module_manager = EducationModuleManager()
        data_store_tiny_db = DataStore('modules')

        modules_list_data = data_store_tiny_db.get_rows()
        # create data store with SQL data adapter
        data_store = DataStore("modules", force_adapter="PostgreSQLDataAdapter")
        for module_data in modules_list_data:
            # convert Course object to Dict
            module = module_manager.module_row_to_module(module_data)
            module_raw = {
                'doc_id': module.id,
                'id_course': module.id_course,
                'name': module.name,
            }

            self.add_row_to_sql(data_store, module.id, module_raw)

    def upload_lessons_list_from_json_to_sql(self) -> None:
        """
        Uploads courses list from json file to sql
        @params:
        """

        # get all courses in the system
        lesson_manager = EducationLessonManager()
        data_store_tiny_db = DataStore('lessons')

        lessons_list_data = data_store_tiny_db.get_rows()
        # create data store with SQL data adapter
        data_store = DataStore("lessons", force_adapter="PostgreSQLDataAdapter")
        for lesson_data in lessons_list_data:
            # convert Course object to Dict
            lesson = lesson_manager.lesson_row_to_lesson(lesson_data)
            lesson_raw = {
                'doc_id': lesson.id,
                'id_module': lesson.id_module,
                'name': lesson.name,
                'text': lesson.text,
                'task': lesson.task,
                'materials': lesson.materials,
                'link': lesson.link
            }

            self.add_row_to_sql(data_store, lesson.id, lesson_raw)

    def get_upload_models_from_json_to_sql_page_data(self, _name_models: str) -> dict:
        """
        Get data for page view

        """
        _data = []

        data_store_tinydb = DataStore(_name_models)
        rows_number = data_store_tinydb.get_rows_count()

        data_store_postgresql = DataStore(_name_models, force_adapter="PostgreSQLDataAdapter")
        current_data_adapter = data_store_postgresql.current_data_adapter
        if current_data_adapter == 'PostgreSQLDataAdapter':
            db_rows_number = data_store_postgresql.get_rows_count()
            is_there_table = 'Created'
        else:
            db_rows_number = None
            is_there_table = 'No created'

        _data = {
            "name_model": _name_models,
            "data_folder": config.DATA_FOLDER,
            "rows_number": rows_number,
            "PostgreSQLDataAdapter_connection_string": config.PostgreSQLDataAdapter_connection_string(),
            "current_data_adapter": current_data_adapter,
            "db_rows_number": db_rows_number,
            "is_there_table": is_there_table
        }

        return _data

    def upload_homeworks_list_from_json_to_sql(self) -> None:
        """
        Uploads homeworks list from json file to sql
        @params:
        """

        # get all courses in the system
        # homework_manager = HomeworkManager()
        con = create_engine("postgresql:" + config.PostgreSQLDataAdapter_connection_string())
        # data_store_tiny_db = DataStore('homeworks')

        # homeworks_list_data = data_store_tiny_db.get_rows()
        homeworks_df = self.get_json_data_in_dataframe('homeworks.json')
        
        homeworks_df['date_delivery'] = pd.to_datetime(homeworks_df['date_delivery'], format='%d/%m/%Y', dayfirst=True)
        homeworks_df['status'] = homeworks_df['status'].astype('bool')
        homeworks_df['doc_id'] = homeworks_df.index
        # create data store with SQL data adapter
        data_store = DataStore("homeworks", force_adapter="PostgreSQLDataAdapter")
        if data_store.get_rows_count() > 0:
            homeworks_sql_df = pd.read_sql('select * from homeworks', con)
            homeworks_df = pd.merge(homeworks_sql_df, homeworks_df, how='outer', indicator=True, left_on='doc_id', right_index=True)
            homeworks_df.drop(homeworks_df[homeworks_df['_merge'] != 'right_only'].index, inplace=True)

        # for homework_data in homeworks_list_data:
        #     # convert Course object to Dict
        #     homework = homework_manager.homework_row_to_homework(homework_data)
        #     homework_raw = {
        #         'doc_id': homework.id,
        #         'id_user': homework.id_user,
        #         'id_lesson': homework.id_lesson,
        #         'users_files_list': homework.users_files_list,
        #         'text': homework.text,
        #         'status': homework.status,
        #         'date_delivery': homework.date_delivery
        #     }

            # self.add_row_to_sql(data_store, homework.id, homework_raw)
            
        homeworks_df.to_sql('homeworks', con, if_exists='append')

    def upload_homework_chat_list_from_json_to_sql(self) -> None:
        """
        Uploads homeworks chats list from json file to sql
        @params:
        """

        # get all courses in the system
        # homework_chat_manager = HomeworkChatManager()
        con = create_engine("postgresql:" + config.PostgreSQLDataAdapter_connection_string())
        # data_store_tiny_db = DataStore('homework_chat')

        homework_chat_df = self.get_json_data_in_dataframe('homework_chat.json')
        homework_chat_df.rename({'id': 'doc_id'})
        # homework_chat_df.drop(homework_chat_df[homework_chat_df.duplicated(keep='last')].index, inplace=True)
        # create data store with SQL data adapter
        # data_store = DataStore("homework_chat", force_adapter="PostgreSQLDataAdapter")
        # if data_store.get_rows_count() != 0:
        #     homework_chat_df_sql = pd.DataFrame(data_store.get_rows())

        homework_chat_df.to_sql('homework_chat', con, if_exists='append', index_label='doc_id')

    def upload_message_from_json_to_sql(self) -> None:
        """
        Uploads messages list from json file to sql
        @params:
        """
        # create data store with SQL data adapter
        data_store = DataStore("users", force_adapter="PostgreSQLDataAdapter")
        con = create_engine("postgresql:" + config.PostgreSQLDataAdapter_connection_string())
        # receive users data from PostgreSQL
        users_df = pd.DataFrame(data_store.get_rows())
        users_df = users_df[['login', 'doc_id']]
        users_df.rename(columns={'doc_id': 'id_user'}, inplace=True)
        # receive messages data from TinyDB
        message_json_df = self.get_json_data_in_dataframe('message.json')
        # preparing messages data for import
        message_json_df['date_send'] = pd.to_datetime(message_json_df['date_send'])
        message_json_df = pd.merge(message_json_df, users_df, how='left', left_on='name_sender', right_on='login')
        message_json_df.drop(columns=['login', 'name_sender', 'files', 'id_user_y', 'id'], inplace=True)
        message_json_df.rename(columns={'id_user_x': 'id_user'}, inplace=True)
        message_json_df['read'] = message_json_df['read'].astype('bool')
        message_json_df_none = message_json_df['id_user'].isnull()
        message_json_df = message_json_df.drop(message_json_df_none[message_json_df_none].index)
        # import messages data to PostgreSQL
        message_json_df.to_sql('message', con, if_exists='append', index_label='doc_id')
        # find homeworks chat without messages and remove
        data_store = DataStore("homework_chat", force_adapter="PostgreSQLDataAdapter")
        homework_chat_doc_id_empty = data_store.get_rows({
            'query': """
            with count_message_for_chat as (
                select count(message.*) over (partition by homework_chat.doc_id) count_message, homework_chat.doc_id
                from message right join homework_chat on id_homework_chat = homework_chat.doc_id
            )
            select count_message_for_chat.doc_id
            from count_message_for_chat
            where count_message = 0
            """
        })
        doc_ids_list = tuple([i['doc_id'] for i in homework_chat_doc_id_empty])

        data_store.delete_row({'where': f"doc_id in {doc_ids_list}"})

    def get_json_data_in_dataframe(self, _name_file):
        # retrieve data from the file
        with open(config.DATA_FOLDER + _name_file, encoding='utf-8') as json_file:
            json_text = json_file.read()
        # prepare data for DataFrame
        if '"_default": {' in json_text:
            json_text = json_text.replace('"_default": {', '')
            ind = json_text.rfind('}')
            json_text = json_text[:ind]

        # create DataFrame with data
        df = pd.read_json(json_text, orient='index')

        return df
