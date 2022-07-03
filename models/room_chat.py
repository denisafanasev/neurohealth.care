

class RoomChat():

    def __init__(self, _id=None, _name='', _message=None, _id_education_stream=None):

        self.id = _id
        self.name = _name
        if _message == []:
            self.message = None
        else:
            self.message = _message
        self.id_education_stream = _id_education_stream

class Message():

    def __init__(self, _id=0, _name_sender='', _text='', _date_send=''):

        self.id = _id
        self.name_sender = _name_sender
        self.text = _text
        self.date_send = _date_send