import os

from data_adapters.data_store import DataStore
from models.course import Course, Lesson, Module
from models.homework import Homework
from models.room_chat import RoomChat, Message
from  models.user import User
import config


def conversion_module_data():
    """
    Конвертация формата данных модулей курсов и перенос в новый файл
    """
    data_store = DataStore('courses_list')
    data_store_module_new = DataStore("modules")

    courses_list = data_store.get_rows()
    for i_course in courses_list:
        course = Course(_id=i_course['id'])
        data_store_module = DataStore(f"course_{course.id}/modules")

        modules_list = data_store_module.get_rows()
        for i_module in modules_list:
            module = Module(_id=i_module['id'], _name=i_module['name'])
            if i_module.get("id_course") is None:
                module.id_course = course.id

            id_modules_edit = data_store_module_new.add_row({"id_course": module.id_course, "name": module.name})

            conversion_lessons_data(module, id_modules_edit)

    # Так как мы перенесли в новый файл данные модулей всех курсов, то удаляем старый файл
    # if os.path.isfile(config.DATA_FOLDER + f"course_{course['id']}/modules.json"):
    #     os.remove(config.DATA_FOLDER + f"course_{course['id']}/modules.json")

def conversion_lessons_data(_module, _id_module_edit):
    """
    Конвертация формата данных уроков курсов и перенос в новый файл
    """
    data_store_lesson_new = DataStore("lessons")
    data_store_lesson = DataStore(f"course_{_module.id_course}/lessons")

    lessons_list = data_store_lesson.get_rows({"id_module": _module.id})
    for i_lesson in lessons_list:
        lesson = Lesson(_id=i_lesson['id'], _id_module=_id_module_edit, _name=i_lesson["name"],
                        _materials=i_lesson['materials'], _link=i_lesson['link'])
        if i_lesson.get("text") is not None:
            lesson.text = i_lesson['text']

        if i_lesson.get("task") is not None:
            lesson.task = i_lesson['task']

        id_lesson_edit = data_store_lesson_new.add_row({"id_module": lesson.id_module, "name": lesson.name,
                                       "materials": lesson.materials, "link": lesson.link,
                                       "text": lesson.text, "task": lesson.task})

        # Так как у нас меняется ID у урока, то нужно найти все домашние задания, которые
        # прикреплены к данному уроку(пока не продумал до конца, как лучше сделать)
        conversion_homework_data(lesson.id, id_lesson_edit, _module.id_course)
        conversion_room_chat_data(lesson.id, id_lesson_edit, _module.id_course)

    # Так как мы перенесли в новый файл данные уроков всех курсов, то удаляем старый файл
    # if os.path.isfile(config.DATA_FOLDER + f"course_{course['id']}/lessons.json"):
    #     os.remove(config.DATA_FOLDER + f"course_{course['id']}/lessons.json")

def conversion_homework_data(_id_lesson, _id_lesson_edit, _id_course):
    """
    Конвертация формата данных домашних работ
    """
    data_store = DataStore("homeworks")
    data_store_answers = DataStore("homework_answers")

    homework_list = data_store.get_rows({"id_course": _id_course, "id_lesson": _id_lesson})
    for homework_data in homework_list:
        homework = Homework(_id=homework_data['id'], _id_lesson=homework_data['id_lesson'], _id_user=homework_data['id_user'])
        if homework_data.get("status") is None:
            homework_answer = data_store_answers.get_rows({"id_homework": homework.id})[0]
            homework.status = homework_answer['answer']

            data_store.update_row({"status": homework.status, "id": homework.id}, "id")

        if homework_data.get("id_course") is not None:
            data_store.delete_key_in_row("id_course", "id", homework.id)

        # conversion_room_chat_data(_id_lesson, _id_lesson_edit, homework.id_user, _id_course)
        data_store.delete_key_in_row("id", "id", homework.id)

def conversion_room_chat_data(_id_lesson, _id_lesson_edit, _id_course):
    """

    """
    data_store = DataStore("room_chat")
    data_store_user = DataStore("users")

    user_list = data_store_user.get_rows()
    for user_data in user_list:
        user = User(_user_id=user_data.doc_id, _login=user_data["login"])
        name_chat = "chat_{id_course}_{id_lesson}_{user_login}".format(
            id_course=_id_course,
            id_lesson=_id_lesson,
            user_login=user.login)
        room_chat_data = data_store.get_rows({"name": name_chat})
        if room_chat_data != []:
            room_chat_data = room_chat_data[0]
            room_chat = RoomChat(_id=room_chat_data['id'], _id_lesson=int(_id_lesson), _id_user=user.user_id)

            id_room_chat = data_store.update_row({"id_lesson": room_chat.id_lesson, "id_user": room_chat.id_user,
                                   "id": room_chat.id}, "id")[0]
            data_store.delete_key_in_row("name", "id", room_chat.id)

            if room_chat_data.get("message") is not None:
                for id_message in room_chat_data["message"]:
                    conversion_message_data(id_message, room_chat_data.doc_id)

            data_store.delete_key_in_row("message", "id", id_room_chat)

            data_store.delete_key_in_row("id", "id", room_chat.id)

def conversion_message_data(_id_message, _id_room_chat):
    """

    """

    data_store = DataStore("message")
    data_store_user = DataStore("users")

    message_data = data_store.get_rows({"id": _id_message})[0]
    message = Message(_id=message_data['id'], _id_room_chat=_id_room_chat)
    if message_data.get("id_room_chat") is None:
        data_store.update_row_by_doc_id({"id_room_chat": message.id_room_chat}, message.id)

    if message_data.get("name_sender") is not None:
        user = data_store_user.get_rows({"login": message_data['name_sender']})[0]

        message.id_user = user.doc_id

        data_store.update_row({"id_user": message.id_user, "id": message.id}, "id")
        data_store.delete_key_in_row("name_sender", "id", message.id)

    data_store.delete_key_in_row("id", "id", _id_message)


# Запуск функций для ковертации форматов данных
conversion_module_data()

