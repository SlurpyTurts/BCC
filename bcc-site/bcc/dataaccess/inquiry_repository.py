import db_connection

class InquiryRepository:

    def get_inquiry_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM websiteInquiries ORDER BY DATE DESC"""
                cursor.execute(sql)
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def get_inquiry_detail(self, id):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM websiteInquiries WHERE id = %s"""
                cursor.execute(sql, id)
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

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

