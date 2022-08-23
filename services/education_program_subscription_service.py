from models.education_program_manager  import EducationProgramManager

class EducationProgramSubscriptionService:
    """
    Service for the education program subscription page
    Возвращает в слой отображения объекты в доменной модели
    Взаимодейтвует с классами слоя моделей, передавая им данные и получая данные в объектах доменной модели
    """

    def get_education_program(self, _id):
        """
        Возвращает обучающий программу по ее id

        Args:
            _id (int): id обущающей программы

        Returns:
            EducationProgram: обучающая программа
        """        

        manager = EducationProgramManager()

        education_program = manager.get_education_program(_id)

        return education_program
