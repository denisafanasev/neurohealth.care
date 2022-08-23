from models.education_program import EducationProgram
from data_adapters.data_store import DataStore

class EducationProgramManager():
    """
    Менеджер управления обучающими программами
    """

    def education_program_row_to_education_program(self, _data_row):
        """
        Преобразовывает структуры хренения в объем EducationProgram

        Args:
            _data_row (dict): словать аттрибутов обучающей программы
        
        Return:
            EducationProgram: объем EducationProgram
        """

        _education_program = EducationProgram(_id=_data_row.doc_id, _name=_data_row['program_name'], _description= "",
            _subscription_payment_link = _data_row['subscription_payment_link'], _education_stream_payment_link = _data_row['education_stream_payment_link'],
            _support_channel_link = _data_row['support_channel_link'])
        
        return _education_program

    def get_education_program(self, _id):
        """
        Возвращает обучающий программу по ее id
        """

        data_store = DataStore("education_programs")
        education_program_data = data_store.get_row_by_id(_id)
        education_program = self.education_program_row_to_education_program(education_program_data)

        return education_program