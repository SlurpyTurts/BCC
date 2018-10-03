import base_data_access
data_access = base_data_access.BaseDataAccess()

class FreightRepository:
    def get_freight_carrier_list(self):
        return data_access.select_request("SELECT * FROM freight")