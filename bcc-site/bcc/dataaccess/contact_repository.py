import db_connection, base_data_access

data_access = base_data_access.BaseDataAccess()

class ContactRepository:

    def get_contact_by_dealer(self, dealer_id):
        return data_access.select_request("SELECT * FROM contact WHERE dealerid = %s", dealer_id)

    def get_contact_by_supplier(self, supplier_id):
        return data_access.select_request("SELECT * FROM contact WHERE supplierid = %s", supplier_id)

    def get_contact_by_order(self, order_number):
        return data_access.select_request("""SELECT firstName, lastName, addressLine1, addressLine2, city, state, zip, country, phoneNumber, email
                        FROM contact
                        WHERE id = (
                            SELECT customerid
                            FROM orderOverview
                            WHERE orderNumber = %s
                        )""", order_number)

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
        return data_access.select_one("SELECT MAX(id) as maxid FROM contact WHERE dealerid IS NULL AND supplierid IS NULL")['maxid']