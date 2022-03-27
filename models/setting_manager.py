from data_adapters.data_store import DataStore
from models.assessment import Assessment

class SettingManager():

    def assessment_row_to_assessment(self, assessment, tests_list):

        assessment = Assessment(assessment["id"],assessment['assessment_parameters'], tests_list)

        return assessment

    def get_assessments(self, _file_name="structure"):

        assessments = []
        data_default = DataStore("structure")
        data_tests = DataStore("structure", "tests")

        if _file_name != "structure":
            _file_name = _file_name.split()[0]
            _file_name = f"{_file_name.split('-')[0]}_{_file_name.split('-')[1]}_age"
            data_criteria = DataStore(_file_name)
        else:
            data_criteria = DataStore("base_criteria")

        assessments_list_data = data_default.get_rows()

        for i_assessment in assessments_list_data:
            tests_list = []

            for i_test in i_assessment["tests"]:
                test = data_tests.get_rows({"id_test": i_test})[0]
                parameters = []

                for i_num, i_criteria in enumerate(test["parameters"].values()):
                    parameters.append({"name_parameters": i_criteria["name_parameters"]})
                    parameters[i_num]["criteria"] = [data_criteria.get_rows({"id": i})[0] for i in i_criteria["criteria"]]

                test["parameters"] = parameters
                tests_list.append(test)

            assessments.append(self.assessment_row_to_assessment(i_assessment, tests_list))

        return assessments

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
                    criteria[i] = _criteria[i_id][i]
                    age_range_file.update_row(criteria)


