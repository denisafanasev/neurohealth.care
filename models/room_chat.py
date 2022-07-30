

class RoomChat():

    def __init__(self, _id=None, _name='', _id_education_stream=None, _id_user=None, _id_lesson=None):

        self.id = _id
        self.name = _name
        self.id_education_stream = _id_education_stream
        self.id_user = _id_user
        self.id_lesson = _id_lesson

class Message():

    def __init__(self, _id=0, _name_sender='', _text='', _date_send=''):

        self.id = _id
        self.name_sender = _name_sender
        self.text = _text
        self.date_send = _date_send