from data_adapters.data_store import DataStore
from models.estimated_values import Estimated_Values
import flask_login
from models.user_manager import UserManager


class EstimatedValuesManager():

    def estimated_values_row_to_estimated_values(self, estimated_values):
        """
        Преобразует структуру данных, в которой хранится информация о испытуемом в структуру Estimated_Values

        Args:
            estimated_values(Dict): словарь с id, названием и списком тестов оценочного параметра

        Returns:
            Estimated_Values: оценочные значения
        """

        estimated_values = Estimated_Values(estimated_values["id"], estimated_values['assessment_parameters'],
                                            estimated_values["tests"])

        return estimated_values

    def get_assessments(self, _file_name):

        estimated_values = []
        data_default = DataStore("structure")
        data_tests = DataStore("structure", "tests")

        if _file_name != "базовые значение":
            _file_name = _file_name.split()[0]
            _file_name = f"{_file_name.split('-')[0]}_{_file_name.split('-')[1]}_age"
            data_criteria = DataStore(_file_name)
        else:
            data_criteria = DataStore("base_criteria")

        estimated_values_list_data = data_default.get_rows()

        for i_estimated_values in estimated_values_list_data:
            tests_list = []

            for i_test in i_estimated_values["tests"]:
                test = data_tests.get_rows({"id_test": i_test})[0]
                parameters = []

                for i_num, i_criteria in enumerate(test["parameters"].values()):
                    parameters.append({"name_parameters": i_criteria["name_parameters"]})
                    parameters[i_num]["criteria"] = [data_criteria.get_rows({"id": i})[0] for i in i_criteria["criteria"]]

                test["parameters"] = parameters
                tests_list.append(test)

            i_estimated_values["tests"] = tests_list

            estimated_values.append(self.estimated_values_row_to_estimated_values(i_estimated_values))

        return estimated_values

    def get_age_ranges(self):

        data = DataStore("age_range")

        age_range_list = data.get_rows()

        age_range = age_range_list[0]["range"]

        return age_range

    def get_age_range(self, _age_range):

        data = DataStore("age_range")

        age_range = data.get_rows(_age_range)
        return age_range

    def overwrite(self, _file_name, _criteria):

        if _file_name == "базовые значение":
            age_range_file = DataStore("base_criteria")
        else:
            _file_name = _file_name.split()[0]
            _file_name = f"{_file_name.split('-')[0]}_{_file_name.split('-')[1]}_age"
            age_range_file = DataStore(_file_name)

        for i_id in range(1, 214):
            criteria = age_range_file.get_rows({"id": i_id})[0]

            for i in criteria.keys():
                if i != "id":
                    criteria[i] = _criteria[i_id - 1]
                    age_range_file.update_row(criteria, "id")

        self.add_notifications(_file_name, "overwrite")

    def add_notifications(self, _age_range, _what):

        data = DataStore("action")
        user_login = UserManager().get_user_by_id(flask_login.current_user.user_id).login

        if data.get_rows({"user": user_login}) is not None:
            if _what == "overwrite":
                data.add_row({"action": "Пользователь {user} изменил данные в файле {file}".format(
                    user=user_login, file=_age_range)})
