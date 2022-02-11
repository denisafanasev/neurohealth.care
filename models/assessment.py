

class Assessment():

    def __init__(self, _assessment_parameters, _tests):

        self.assessment_parameters = _assessment_parameters
        self.tests = []

        for i_test in _tests:
            self.test = {}

            self.test["name_test"] = i_test[0]["name_test"]
            self.test["parameters"] = i_test[0]["parameters"]
            self.test["id_test"] = i_test[0]["id"]

            self.tests.append(self.test)

        del self.test