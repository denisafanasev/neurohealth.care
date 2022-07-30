import os

from data_adapters.data_store import DataStore
from models.course import Course, Lesson, Module
from models.homework import Homework
from models.room_chat import RoomChat, Message
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
            module = Module(_name=i_module['name'])
            if i_module.get("id_course") is None:
                module.id_course = course.id

            data_store_module_new.add_row({"id_course": module.id_course, "name": module.name})

    # Так как мы перенесли в новый файл данные модулей всех курсов, то удаляем старый файл
    # if os.path.isfile(config.DATA_FOLDER + f"course_{course['id']}/modules.json"):
    #     os.remove(config.DATA_FOLDER + f"course_{course['id']}/modules.json")

def conversion_lessons_data():
    """
    Конвертация формата данных уроков курсов и перенос в новый файл
    """
    data_store = DataStore('courses_list')
    data_store_lesson_new = DataStore("lessons")
    data_store_chat = DataStore("room_chat")
    data_store_homework = DataStore("homeworks")

    courses_list = data_store.get_rows()
    for i_course in courses_list:
        course = Course(_id=i_course['id'])
        data_store_lesson = DataStore(f"course_{course.id}/lessons")

        lessons_list = data_store_lesson.get_rows()
        for i_lesson in lessons_list:
            lesson = Lesson(_id=i_lesson['id'], _id_module=i_lesson['id_module'], _name=i_lesson["name"], _materials=i_lesson['materials'],
                            _link=i_lesson['link'])
            if i_lesson.get("text") is not None:
                lesson.text = i_lesson['text']

            if i_lesson.get("task") is not None:
                lesson.task = i_lesson['task']

            lesson_edit = data_store_lesson_new.add_row({"id_module": lesson.id_module, "name": lesson.name,
                                           "materials": lesson.materials, "link": lesson.link,
                                           "text": lesson.text, "task": lesson.task})

            # Так как у нас меняется ID у урока, то нужно найти все комнаты чатов и домашние задания, которые
            # прикреплены к данному уроку(пока не продумал до конца, как лучше сделать)
            # room_chat_list = data_store_chat.get_rows({"id_lesson": lesson.id})
            # for i_room_chat in room_chat_list:
            #     room_chat = RoomChat(_id=i_room_chat['id'], _name=i_room_chat['name'])

        # Так как мы перенесли в новый файл данные уроков всех курсов, то удаляем старый файл
        # if os.path.isfile(config.DATA_FOLDER + f"course_{course['id']}/lessons.json"):
        #     os.remove(config.DATA_FOLDER + f"course_{course['id']}/lessons.json")

def conversion_homework_data():
    """
    Конвертация формата данных домашних работ
    """
    data_store = DataStore("homeworks")
    data_store_answers = DataStore("homework_answers")

    homework_list = data_store.get_rows()
    for i_homework in homework_list:
        homework = Homework(_id=i_homework['id'], _id_lesson=i_homework['id_lesson'])
        if i_homework.get("status") is None:
            homework_answer = data_store_answers.get_rows({"id_homework": homework.id})[0]
            i_homework['status'] = homework_answer['answer']

            data_store.update_row({"id": i_homework})

        if i_homework.get("id_room_chat") is not None:
            data_store.delete_key_in_row("id_room_chat", "id", i_homework['id'])

        if i_homework.get("id_course") is not None:
            data_store.delete_key_in_row("id_course", "id", i_homework['id'])


# Запуск функций для ковертации форматов данных
conversion_module_data()
conversion_lessons_data()

