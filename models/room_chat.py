

class RoomChat():

    def __init__(self, _id=None, _id_education_stream=None, _id_user=None, _id_lesson=None):

        self.id = _id
        self.id_education_stream = _id_education_stream
        self.id_user = _id_user
        self.id_lesson = _id_lesson

class Message():

    def __init__(self, _id=0, _id_user='', _text='', _date_send='', _id_room_chat=None):

        self.id = _id
        self.id_user = _id_user
        self.text = _text
        self.date_send = _date_send
        self.id_room_chat = _id_room_chat