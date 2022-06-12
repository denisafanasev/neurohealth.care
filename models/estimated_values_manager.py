from data_adapters.data_store import DataStore
from models.estimated_values import Estimated_Values
from services.action_service import ActionService

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

    def get_assessments(self, _id_file_name):
        """
        Возвращает оценочные значения для тестов

        Args:
            _id_file_name(Int): индентификатор названия файла с тестами
        """

        estimated_values = []
        data_default = DataStore("structure")
        data_tests = DataStore("structure", "tests")

        if data_default.get_rows() == []:
            return None

        data_criteria = DataStore(self.get_age_range(_id_file_name)['name_file'])

        if data_criteria.get_rows() == []:
            data_criteria_base = DataStore(self.get_age_range(1)['name_file'])
            data_base = data_criteria_base.get_rows()

            for i in data_base:
                data_criteria.add_row(i)

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
        """
        Возвращает список диапазонов возрастов

        Returns:
            List: список диапазонов возрастов
        """

        data = DataStore("age_range")

        age_ranges = data.get_rows()
        age_range_list = []

        for i_age_range in age_ranges:
            age_range = {
                "id": i_age_range["id"],
                "range": i_age_range["range"]
            }

            age_range_list.append(age_range)

        return age_range_list

    def get_age_range(self, _id_file_name):
        """
        Возвращает данные диапазона возрастов

        Args:
            _id_file_name(Int): индентификатор названия файла с тестами

        Returns:
            age_range(Dict): данные диапазона возрастов
        """

        data = DataStore("age_range")

        age_range = data.get_rows({"id": _id_file_name})[0]
        return age_range

    def overwrite(self, _id_file_name, _criteria):
        """
        Изменяет оценочные значения в тестах

        Args:
            _id_file_name(Int): индентификатор названия файла с тестами
            _criteria(Dict): словарь с измененными оценочными значениями
        """

        age_range_file = DataStore(self.get_age_range(_id_file_name)["name_file"])

        for i_id in range(1, 214):
            criteria = age_range_file.get_rows({"id": i_id})[0]

            for i in criteria.keys():
                if i != "id":
                    criteria[i] = _criteria[i_id - 1]
                    age_range_file.update_row(criteria, "id")

        return self.get_age_range(_id_file_name)['range']