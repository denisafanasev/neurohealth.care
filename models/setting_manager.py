from data_adapters.data_store import DataStore
from models.assessment import Assessment

class SettingManager():

    def assessment_row_to_assessment(self, assessment, tests_list):

        assessment = Assessment(assessment['assessment_parameters'], tests_list)

        return assessment

    def get_assessments(self):

        assessments = []
        data_default = DataStore("structure")
        data_tests = DataStore("structure", "tests")

        assessments_list_data = data_default.get_rows()

        for i_assessment in assessments_list_data:
            tests_list = []
            for i_test in i_assessment["tests"]:
                tests_list.append(data_tests.get_rows({"id":i_test}))

            assessments.append(self.assessment_row_to_assessment(i_assessment, tests_list))

        return assessments



