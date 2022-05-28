

class RoomChat():

    def __init__(self, _id=0, _name='', _message=None):

        self.id = _id
        self.name = _name
        if _message == []:
            self.message = None
        else:
            self.message = _message

class Message():

    def __init__(self, _id=0, _name_sender='', _text='', _files=None):

        self.id = _id
        self.name_sender = _name_sender
        self.text = _text
        if _files == []:
            self.files = None
        else:
            self.files = _files

class UserFile():

    def __init__(self, _name_file_user='', _name_file_unique='', _path=''):

        self.name_file_user = _name_file_user
        self.name_file_unique = _name_file_unique
        self.path = _path