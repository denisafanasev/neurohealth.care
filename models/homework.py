
class Homework():

    def __init__(self, _id=None, _id_room_chat=None, _users_files_list=None, _text=None):

        self.id = int(_id)
        self.id_room_chat = _id_room_chat
        self.users_files_list = _users_files_list
        self.text = _text


class HomeworkAnswer():

    def __init__(self, _id=None, _answer=None, _id_homework=None):

        self.id = _id
        self.id_homework = _id_homework
        self.answer = _answer


