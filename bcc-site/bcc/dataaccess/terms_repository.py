import base_data_access
data_access = base_data_access.BaseDataAccess()

class TermsRepository:
    def get_terms_list(self):
        return data_access.select_request("SELECT * FROM terms")