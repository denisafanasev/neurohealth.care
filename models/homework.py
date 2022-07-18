
class Homework():

    def __init__(self, _id=None, _id_room_chat=None, _users_files_list=None, _text=None, _id_user=None, _id_course=None,
                 _id_lesson=None):

        self.id = int(_id)
        self.id_user = _id_user
        self.id_course = _id_course
        self.id_lesson = _id_lesson
        self.id_room_chat = _id_room_chat
        self.users_files_list = _users_files_list
        self.text = _text


class HomeworkAnswer():

    def __init__(self, _id=None, _answer=None, _id_homework=None):

        self.id = _id
        self.id_homework = _id_homework
        self.answer = _answer


