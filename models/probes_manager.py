from data_adapters.data_store import DataStore
from models.probe import Probe
from models.estimated_values_manager import EstimatedValuesManager

class ProbesManager():

    def get_probes(self):
        data = DataStore("probe")

        probe_list = data.get_rows()

        for i_probe in probe_list:
            pass

    def probe_row_to_probe(self, _name_probationer, _probationer_id, _date_of_birth, _protocol_status):

        probe = Probe(_name_probationer, _probationer_id, _date_of_birth, _protocol_status)

        return probe

    def add_probe(self, _probationer, _protocol_status):

        data = DataStore("probe")

        probe = self.probe_row_to_probe(_probationer["name_probationer"], _probationer["probationer_id"],
                                        _probationer["date_of_birth"], _protocol_status)

        for i_range in EstimatedValuesManager().get_age_ranges():
            if i_range != "базовые значения":
                age_range = i_range.split()[0]
                age_range = age_range.split("_")

                if int(age_range[0]) <= probe.age_probationer and int(age_range[1]) >= probe.age_probationer:
                    pass


        data.add_row({"name_probationer": probe.name_probationer, "probationer_id": probe.probationer_id,
                      "protocol_status": probe.protocol_status})


