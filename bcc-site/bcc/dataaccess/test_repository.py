import base_data_access
data_access = base_data_access.BaseDataAccess()

class TestRepository:
    def set_amp_test(self):
        data_access.select_request("SELECT * FROM todo ORDER BY dateUpdated DESC")