import db_connection

class ContactRepository:

    def get_contact_by_dealer(self, dealer_id):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM contact WHERE dealerid = %s"
                cursor.execute(sql, dealer_id)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_contact_by_supplier(self, supplier_id):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM contact WHERE supplierid = %s"
                cursor.execute(sql, supplier_id)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_contact_by_order(self, order_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT firstName, lastName, addressLine1, addressLine2, city, state, zip, country, phoneNumber, email
                        FROM contact
                        WHERE id = (
                            SELECT customerid
                            FROM orderOverview
                            WHERE orderNumber = %s
                        )"""
                cursor.execute(sql, order_number)
                return cursor.fetchall()
        finally:
            connection.close()

    def set_new_cust_contact(self, cust_first_name, cust_last_name, cust_shipping_address_line_1, cust_shipping_address_line_2, cust_city, cust_state, cust_zip, cust_country, cust_phone, cust_email):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO contact
                (firstName, lastName, addressLine1, addressLine2, city, state, zip, country, phoneNumber, email)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (cust_first_name, cust_last_name, cust_shipping_address_line_1, cust_shipping_address_line_2, cust_city, cust_state, cust_zip, cust_country, cust_phone, cust_email))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def get_max_cust_id(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT MAX(id) as maxid FROM contact WHERE dealerid IS NULL AND supplierid IS NULL"
                cursor.execute(sql)
                result = cursor.fetchone()
                return result['maxid']
        finally:
            connection.close()