from datetime import datetime, timedelta


class EducationStream():

    def __init__(self, _id=None, _name='', _date_start='', _date_end='', _id_course=None, _curators_list=None,
                 _students_list=None, _teacher=None, _status=''):

        self.id = _id
        self.name = _name
        self.course = _id_course
        self.curators_list = _curators_list
        self.students_list = _students_list
        self.teacher = _teacher
        self.status = _status

        if _date_start != '':
            if type(_date_start) is str:
                self.date_start = datetime.strptime(_date_start, '%d/%m/%Y')
            else:
                self.date_start = _date_start
        else:
            self.date_start = datetime.today()

        if _date_end != '':
            if type(_date_end) is str:
                self.date_end = datetime.strptime(_date_end, '%d/%m/%Y')
            else:
                self.date_end = _date_end
        else:
            self.date_end = datetime.today() + timedelta(days=1)
