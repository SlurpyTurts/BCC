import db_connection

class DealerRepository:

    def get_dealer_list(self, start_id, number_of_dealers):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM dealer WHERE id > %s AND id <= %s"
                cursor.execute(sql, (start_id, start_id + number_of_dealers))
                return cursor.fetchall()
        finally:
            connection.close()

    def get_full_dealer_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM dealer"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_dealer_detail(self, dealer_id):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM dealer WHERE id = %s"
                cursor.execute(sql, dealer_id)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_order_list(self, dealer_id):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT orderNumber, contact.lastName, orderDate, invoiceSentDate, orderStatus
                FROM orderOverview
                INNER JOIN contact ON orderOverview.customerid = contact.id
                WHERE orderOverview.dealerID = %s;"""
                cursor.execute(sql, dealer_id)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_dealer_status_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT DISTINCT status from dealer"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def set_new_dealer(self, dealer_name, dealer_website, dealer_status, billing_address_line_1, billing_address_line_2, billing_city, billing_state, billing_zip, billing_country, shipping_address_line_1, shipping_address_line_2, shipping_city, shipping_state, shipping_zip, shipping_country):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO dealer (
                dealerName, dealerWebsite, status,
                billingAddressLine1, billingAddressLine2, billingCity, billingState, billingZip, billingCountry,
                shippingAddressLine1, shippingAddressLine2, shippingCity, shippingState, shippingZip, shippingCountry,
                dateUpdated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())"""
                cursor.execute(sql, (dealer_name, dealer_website, dealer_status, billing_address_line_1, billing_address_line_2, billing_city, billing_state, billing_zip, billing_country, shipping_address_line_1, shipping_address_line_2, shipping_city, shipping_state, shipping_zip, shipping_country))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def set_update_dealer(self, dealer_name, dealer_website, dealer_status, billing_address_line_1, billing_address_line_2, billing_city, billing_state, billing_zip, billing_country, shipping_address_line_1, shipping_address_line_2, shipping_city, shipping_state, shipping_zip, shipping_country, dealer_id):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """UPDATE dealer
                        SET
                            dealerName=%s,
                            dealerWebsite=%s,
                            status=%s,
                            billingAddressLine1=%s,
                            billingAddressLine2=%s,
                            billingCity=%s,
                            billingState=%s,
                            billingZip=%s,
                            billingCountry=%s,
                            shippingAddressLine1=%s,
                            shippingAddressLine2=%s,
                            shippingCity=%s,
                            shippingState=%s,
                            shippingZip=%s,
                            shippingCountry=%s
                        WHERE id=%s"""
                cursor.execute(sql, (dealer_name, dealer_website, dealer_status, billing_address_line_1, billing_address_line_2, billing_city, billing_state, billing_zip, billing_country, shipping_address_line_1, shipping_address_line_2, shipping_city, shipping_state, shipping_zip, shipping_country, dealer_id))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()