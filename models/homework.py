
class Homework():

    def __init__(self, _id=None, _id_room_chat=None, _users_files_list=None, _date_delivery=None, _homework_answer=None):

        self.id = _id
        self.id_room_chat = _id_room_chat
        self.users_files_list = _users_files_list
        self.date_delivery = _date_delivery
        self.homework_answer = _homework_answer


class HomeworkAnswer():

    def __init__(self, _id=None, _answer=None, _id_homework=None, _status=""):

        self.id = _id
        self.id_homework = _id_homework
        self.answer = _answer
        self.status = _status


