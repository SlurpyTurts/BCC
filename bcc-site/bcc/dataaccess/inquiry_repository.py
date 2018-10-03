import db_connection, base_data_access

data_access = base_data_access.BaseDataAccess()

class InquiryRepository:

    def get_inquiry_list(self):
        return data_access.select_request("""SELECT * FROM websiteInquiries ORDER BY DATE DESC""")

    def get_inquiry_detail(self, id):
        return data_access.select_request("""SELECT * FROM websiteInquiries WHERE id = %s""", id)

    def set_new_inquiry(self, first_name, last_name, subject, message, email, city, state, country, date):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql =   """
                        INSERT INTO websiteInquiries (firstName, lastName, subject, message, email, city, state, country, date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                cursor.execute(sql, (first_name, last_name, subject, message, email, city, state, country, date))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

