
class Homework():

    def __init__(self, _id=None, _users_files_list=None, _text=None, _id_user=None, _id_lesson=None, _status=None):

        self.id = int(_id)
        self.id_user = _id_user
        self.id_lesson = _id_lesson
        self.users_files_list = _users_files_list
        self.text = _text
        self.status = _status