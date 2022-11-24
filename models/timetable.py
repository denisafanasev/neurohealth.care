from datetime import datetime


class Timetable():

    def __init__(self, _id=None, _id_education_stream=None, _id_module=None,_date_start=''):

        self.id = _id
        self.id_education_stream = _id_education_stream
        self.id_module = _id_module
        if _date_start != '':
            self.date_start = _date_start
        else:
            self.date_start = datetime.today()
