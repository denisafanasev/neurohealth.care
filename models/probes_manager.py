from data_adapters.data_store import DataStore
from models.probe_probationer import Probe
from models.estimated_values_manager import EstimatedValuesManager
from models.probe_test import Test


class ProtocolsManager():

    def protocol_row_to_protocol(self, _data_row):

        probe = Probe(_data_row.doc_id, _data_row['name_probationer'], _data_row['probationer_id'],
                      _protocol_status=_data_row['protocol_status'], _test=_data_row['test'])

        return probe

    def get_protocols(self):
        data_store = DataStore("probes")
        probes = []

        probe_list = data_store.get_rows()

        for i_probe in probe_list:
            i_probe["date_of_birth"] = ""
            i_probe['test'] = ""
            probe = self.protocol_row_to_protocol(i_probe)

            probes.append(probe)

        return probes

    def add_protocol(self, _probationer_id, _probe_id, _protocol_status="черновик"):

        data_store = DataStore("probes")

        probe_id = data_store.get_rows_count() + 1
        test = f"test_probe_id_{probe_id}"
        # data = {
        #     'name_probationer': '',
        #     'probationer_id': _probationer_id,
        #     'date_of_birth': '',
        #     'protocol_status': _protocol_status,
        #     'test': f'test_probe_id_{probe_id}'
        # }
        probe = Probe(_probationer_id=_probationer_id, _probe_id=_probe_id, _test=test, _protocol_status=_protocol_status)

        data_store.insert_row({"probe_id": probe.probe_id, "name_probationer": probe.name_probationer,
                               "probationer_id": probe.probationer_id,
                               "protocol_status": probe.protocol_status,
                               "estimated_values_file": '',
                               "date_test": probe.date_test, "date_protocol": probe.date_protocol, "test": probe.test})

        return probe.probe_id

    def test_row_to_test(self, _id, _assessment_parameters, _tests):
        test = Test(_id, _assessment_parameters, _tests)

        return test

    def get_protocol(self, _protocol_id):

        data_store_probes = DataStore("test")
        data_store_parameters = DataStore("test", "parameters")
        data_store_grade = DataStore("parameters_criteria")
        data_store_radio = DataStore("parameters_criteria", "radio_value")
        data_store_probe = DataStore("probes")

        # test = data_store_probes.get_rows({"id": _id_test})[0]
        protocol_data = data_store_probe.get_rows({"probe_id": _protocol_id})[0]
        protocol = self.protocol_row_to_protocol(protocol_data)

        data_store_grade_probationer = DataStore("probes", protocol.test)
        grades_probationer = data_store_grade_probationer.get_rows()
        if grades_probationer:
            grade = data_store_grade.get_rows({'id': grades_probationer[0]['id']})[0]
            parameter = data_store_parameters.get_rows({'id': grade['id_parameters']})[0]
            test = data_store_probes.get_rows({'id': parameter['id_test']})[0]

            parameters = data_store_parameters.get_rows({"id_test": test["id"]})
        else:
            return None
        parameter_list = []
        for i_parameter in parameters:
            grades = data_store_grade.get_rows({"id_parameters": i_parameter["id"]})
            grades_list = []

            for i_grade in grades:

                if grades_probationer != []:
                    grade = data_store_grade_probationer.get_rows({"id": i_grade["id"]})
                    if grade != []:
                        i_grade["grade"] = grade[0]["grade"]

                if i_grade["radio_value"]:
                    radio_values = []

                    for i_radio_value in i_grade["radio_value"]:
                        radio_values.append(data_store_radio.get_rows({"id": i_radio_value})[0])

                    i_grade["radio_value"] = radio_values

                grades_list.append(i_grade)

            i_parameter["grades"] = grades_list
            parameter_list.append(i_parameter)

        test["parameters"] = parameter_list

        protocol.test = self.test_row_to_test(test["id"], test["name_probe"], test["parameters"])

        return protocol

    def get_tests_list(self):

        data_store_probes = DataStore("test")
        tests_list = data_store_probes.get_rows()

        return tests_list

    def add_grades_in_probe(self, _grades, _probe_id, _protocol_status):

        data_store = DataStore("probes")

        # if _protocol_status != "":
        #     data_store.update_row({"protocol_status": _protocol_status, "probe_id": _probe_id}, "probe_id")

        test_file = data_store.get_rows({"probe_id": _probe_id})
        data_store_test = DataStore("probes", test_file[0]["test"])

        for grade in _grades:
            if "_" in grade["id"]:
                data_store_test.insert_row(
                    {"id": int(grade["id"].split("_")[0]), "grade": {grade["id"].split("_")[1]: grade["grade"]}})
            else:
                data_store_test.insert_row({"id": int(grade["id"]), "grade": grade["grade"]})

    def get_probe_by_id(self, _probe_id):
        """
        Возвращает протокол по ID

        Args:
            _probe_id(Int): ID протокола

        Returns:
            Probe: протокол
        """
        data_store = DataStore("probes")
        probe = data_store.get_rows({"probe_id": _probe_id})
        probe['test'] = ''

        return self.protocol_row_to_protocol(probe)

    def get_probes_by_probationer_id(self, _probationer_id):
        """
        Возвращает данные протокола по ID тестируемого

        Args:
            _probationer_id(Int): ID тестируемого

        Returns:
            List(Probe): протокол
        """
        data_store = DataStore('probes')
        probes_data = data_store.get_rows({"probationer_id": _probationer_id})
        if probes_data is not None:
            probes_list = []
            for probe in probes_data:
                probes_list.append(self.protocol_row_to_protocol(probe))

            return probes_list

    def get_probes_list(self):
        """
        Возвращает список доступных проб для тестирования

        Returns:
            List(Probe): список проб
        """
        data_store = DataStore('test')

        probes_data = data_store.get_rows()
        probes_list = []
        if probes_data is not None:
            for probe in probes_data:
                probes_list.append(Test(probe.doc_id, probe['name_probe'], ''))

        return probes_list

    def get_protocol_by_id(self, _protocol_id):
        """
        Возвращает данные протокола по ID

        Args:
            _protocol_id(Int): ID протокола

        Returns:
            Probe: протокол
        """
        data_store = DataStore('probes')

        protocol_data = data_store.get_rows({'probe_id': _protocol_id})
        if protocol_data:
            return self.protocol_row_to_protocol(protocol_data[0])

    def get_probe_by_id_grade(self, _protocol_test):

        data_store_tests = DataStore("test")
        data_store_parameters = DataStore("test", "parameters")
        data_store_grade = DataStore("parameters_criteria")

        data_store_grade_probationer = DataStore("probes", _protocol_test)
        grades_probationer = data_store_grade_probationer.get_rows()
        if grades_probationer:
            grade = data_store_grade.get_rows({'id': grades_probationer[0]['id']})[0]
            parameter = data_store_parameters.get_rows({'id': grade['id_parameters']})[0]
            test = data_store_tests.get_rows({'id': parameter['id_test']})[0]

        else:
            test = data_store_tests.get_rows({'id': 1})[0]

        return self.test_row_to_test(test.doc_id, test['name_probe'], '')
