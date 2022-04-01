from datetime import datetime

class Probe():

    def __init__(self, _name_probationer="", _probationer_id=0, _date_of_birth="", _protocol_status=""):

        self.name_probationer = _name_probationer
        self.probationer_id = _probationer_id
        self.age_probationer = (datetime.now() - _date_of_birth).year

        if _protocol_status == "add":
            self.protocol_status = "окончательный"
        elif _protocol_status == "draft":
            self.protocol_status = "черновик"